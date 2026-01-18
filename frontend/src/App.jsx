import { useState, useEffect } from 'react'
import Header from './components/Header'
import TaskList from './components/TaskList'
import PomodoroTimer from './components/PomodoroTimer'
import DistractionModal from './components/DistractionModal'
import ApiTest from './components/ApiTest'
import './App.css'

function App() {
  const [tasks, setTasks] = useState([
    {
      id: 1,
      title: 'Implementar autenticación API',
      completed: false,
      category: 'laboral',
      customCategory: '',
      subtasks: [
        { id: 1, title: 'Configurar JWT', completed: false, timeSpent: 0 },
        { id: 2, title: 'Crear middleware de auth', completed: false, timeSpent: 0 }
      ],
      timeSpent: 0
    },
    {
      id: 2,
      title: 'Optimizar consultas DB',
      completed: false,
      category: 'laboral',
      customCategory: '',
      subtasks: [
        { id: 3, title: 'Indexar tablas principales', completed: false, timeSpent: 0 },
        { id: 4, title: 'Revisar queries N+1', completed: false, timeSpent: 0 }
      ],
      timeSpent: 0
    }
  ])

  const [currentPomodoro, setCurrentPomodoro] = useState({
    objective: '',
    taskId: null,
    subtaskIds: [],
    timer: 5, // 5 segundos para pruebas (normalmente 25 * 60)
    isRunning: false,
    mode: 'pomodoro' // pomodoro, shortBreak, longBreak
  })

  const [pomodoroCount, setPomodoroCount] = useState(0)
  const [showDistractionModal, setShowDistractionModal] = useState(false)
  const [distractionModalShown, setDistractionModalShown] = useState([])

  // Lógica para mostrar modal de distracciones
  // Cada 10 pomodoros, 3 veces debe aparecer el modal
  useEffect(() => {
    if (pomodoroCount === 0) return

    const currentGroup = Math.floor((pomodoroCount - 1) / 10)
    const modalsInCurrentGroup = distractionModalShown.filter(
      count => Math.floor((count - 1) / 10) === currentGroup
    ).length

    // Si ya se mostraron 3 modales en este grupo, no mostrar más
    if (modalsInCurrentGroup >= 3) return

    // Pre-seleccionar 3 pomodoros aleatorios en cada grupo de 10
    // Para simplificar, usaremos probabilidad ajustada
    const positionInGroup = ((pomodoroCount - 1) % 10) + 1
    const remainingModals = 3 - modalsInCurrentGroup
    const remainingPositions = 11 - positionInGroup
    
    // Si ya pasaron posiciones suficientes, forzar mostrar
    if (remainingModals >= remainingPositions) {
      if (!distractionModalShown.includes(pomodoroCount)) {
        setShowDistractionModal(true)
        setDistractionModalShown(prev => [...prev, pomodoroCount])
      }
      return
    }

    // Probabilidad de mostrar: remainingModals / remainingPositions
    const probability = remainingModals / remainingPositions
    const shouldShow = Math.random() < probability

    if (shouldShow && !distractionModalShown.includes(pomodoroCount)) {
      setShowDistractionModal(true)
      setDistractionModalShown(prev => [...prev, pomodoroCount])
    }
  }, [pomodoroCount, distractionModalShown])

  const handlePomodoroComplete = () => {
    setPomodoroCount(prev => prev + 1)
    
    // Actualizar tiempo de tareas y subtareas
    if (currentPomodoro.taskId) {
      setTasks(prevTasks => {
        return prevTasks.map(task => {
          if (task.id === currentPomodoro.taskId) {
            const updatedSubtasks = task.subtasks.map(subtask => {
              if (currentPomodoro.subtaskIds.includes(subtask.id)) {
                return {
                  ...subtask,
                  timeSpent: subtask.timeSpent + 5 // 5 segundos para pruebas (normalmente 25 * 60)
                }
              }
              return subtask
            })
            
            const totalTime = updatedSubtasks.reduce((sum, st) => sum + st.timeSpent, 0)
            
            return {
              ...task,
              subtasks: updatedSubtasks,
              timeSpent: totalTime
            }
          }
          return task
        })
      })
    }
  }

  const handleDistractionModalClose = () => {
    setShowDistractionModal(false)
  }

  const updateTasks = (updatedTasks) => {
    setTasks(updatedTasks)
  }

  const updateCurrentPomodoro = (updatedPomodoro) => {
    setCurrentPomodoro(updatedPomodoro)
  }

  return (
    <div className="app">
      <Header />
      <ApiTest />
      <div className="app-content">
        <TaskList 
          tasks={tasks}
          onTasksChange={updateTasks}
          currentPomodoro={currentPomodoro}
          onCurrentPomodoroChange={updateCurrentPomodoro}
        />
        <PomodoroTimer
          currentPomodoro={currentPomodoro}
          onCurrentPomodoroChange={updateCurrentPomodoro}
          tasks={tasks}
          onPomodoroComplete={handlePomodoroComplete}
        />
      </div>
      {showDistractionModal && (
        <DistractionModal onClose={handleDistractionModalClose} />
      )}
    </div>
  )
}

export default App
