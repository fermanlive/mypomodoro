import { useState, useEffect, useRef } from 'react'
import './PomodoroTimer.css'

function PomodoroTimer({ currentPomodoro, onCurrentPomodoroChange, tasks, onPomodoroComplete }) {
  const [timer, setTimer] = useState(currentPomodoro.timer)
  const [isRunning, setIsRunning] = useState(false)
  const [mode, setMode] = useState('pomodoro')
  const [objective, setObjective] = useState(currentPomodoro.objective || '')
  const [editingObjective, setEditingObjective] = useState(false)
  const [pomodoroNumber, setPomodoroNumber] = useState(1)
  const intervalRef = useRef(null)

  const modes = {
    pomodoro: { label: 'Pomodoro', duration: 5 }, // 5 segundos para pruebas
    shortBreak: { label: 'Short Break', duration: 5 }, // 5 segundos para pruebas
    longBreak: { label: 'Long Break', duration: 15 } // 15 segundos para pruebas
  }

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = setInterval(() => {
        setTimer(prev => {
          if (prev <= 1) {
            setIsRunning(false)
            // Solo contar pomodoros completos (no breaks)
            if (mode === 'pomodoro') {
              onPomodoroComplete()
            }
            return modes[mode].duration
          }
          return prev - 1
        })
      }, 1000)
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [isRunning, mode, onPomodoroComplete])

  useEffect(() => {
    setTimer(modes[mode].duration)
    setIsRunning(false)
  }, [mode])

  const handleStart = () => {
    setIsRunning(true)
    onCurrentPomodoroChange({
      ...currentPomodoro,
      isRunning: true,
      timer,
      objective
    })
  }

  const handlePause = () => {
    setIsRunning(false)
    onCurrentPomodoroChange({
      ...currentPomodoro,
      isRunning: false
    })
  }

  const handleModeChange = (newMode) => {
    setMode(newMode)
    onCurrentPomodoroChange({
      ...currentPomodoro,
      mode: newMode
    })
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  }

  const getSelectedTaskName = () => {
    if (currentPomodoro.taskId) {
      const task = tasks.find(t => t.id === currentPomodoro.taskId)
      if (task) {
        const subtaskNames = task.subtasks
          .filter(st => currentPomodoro.subtaskIds.includes(st.id))
          .map(st => st.title)
        if (subtaskNames.length > 0) {
          return `${task.title} - ${subtaskNames.join(', ')}`
        }
        return task.title
      }
    }
    return ''
  }

  const handleObjectiveSubmit = () => {
    setEditingObjective(false)
    onCurrentPomodoroChange({
      ...currentPomodoro,
      objective
    })
  }

  return (
    <div className="pomodoro-container">
      <div className="pomodoro-header">
        <div className="pomodoro-modes">
          {Object.entries(modes).map(([key, value]) => (
            <button
              key={key}
              className={`mode-btn ${mode === key ? 'active' : ''}`}
              onClick={() => handleModeChange(key)}
            >
              {value.label}
            </button>
          ))}
        </div>
      </div>

      <div className="pomodoro-content">
        <div className="pomodoro-objective-section">
          <label className="objective-label">
            En este pomodoro deseo terminar:
          </label>
          {editingObjective ? (
            <div className="objective-input-container">
              <input
                type="text"
                value={objective}
                onChange={(e) => setObjective(e.target.value)}
                onBlur={handleObjectiveSubmit}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') handleObjectiveSubmit()
                }}
                className="objective-input"
                placeholder="Define el objetivo de este pomodoro..."
                autoFocus
              />
              <button className="objective-edit-btn" onClick={handleObjectiveSubmit}>
                ✓
              </button>
            </div>
          ) : (
            <div className="objective-display-container">
              <input
                type="text"
                value={objective || getSelectedTaskName() || 'Define el objetivo...'}
                readOnly
                className="objective-display"
              />
              <button
                className="objective-edit-btn"
                onClick={() => setEditingObjective(true)}
              >
                Edit
              </button>
            </div>
          )}
        </div>

        <div className="pomodoro-timer-display">
          <div className="timer-circle">
            <span className="timer-text">{formatTime(timer)}</span>
          </div>
        </div>

        <div className="pomodoro-controls">
          {isRunning ? (
            <button className="timer-btn pause" onClick={handlePause}>
              PAUSE
            </button>
          ) : (
            <button className="timer-btn start" onClick={handleStart}>
              START
            </button>
          )}
        </div>

        <div className="pomodoro-info">
          <span className="pomodoro-number">#{pomodoroNumber}</span>
          <span className="pomodoro-message">Time to code!</span>
        </div>

        {getSelectedTaskName() && (
          <div className="selected-task-info">
            <span className="selected-task-label">Tarea seleccionada:</span>
            <span className="selected-task-name">{getSelectedTaskName()}</span>
          </div>
        )}
      </div>
    </div>
  )
}

export default PomodoroTimer
