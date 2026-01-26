import { useState, useEffect } from 'react'
import Header from './components/Header'
import TaskList from './components/TaskList'
import PomodoroTimer from './components/PomodoroTimer'
import DistractionModal from './components/DistractionModal'
import { isAuthenticated } from './services/auth'
import { 
  getTasksFromCache, 
  saveTasksToCache, 
  getPomodoroCountFromCache, 
  savePomodoroCountToCache,
  getCurrentPomodoroFromCache,
  saveCurrentPomodoroToCache
} from './services/cache'
import './App.css'

function App() {
  // Cargar datos del cache si existen
  const initialTasks = getTasksFromCache().length > 0 
    ? getTasksFromCache() 
    : [
      // Tareas de referencia para futuro desarrollo
      // {
      //   id: 1,
      //   title: 'Implementar autenticación API',
      //   completed: false,
      //   category: 'laboral',
      //   customCategory: '',
      //   subtasks: [
      //     { id: 1, title: 'Configurar JWT', completed: false, timeSpent: 0 },
      //     { id: 2, title: 'Crear middleware de auth', completed: false, timeSpent: 0 }
      //   ],
      //   timeSpent: 0
      // },
      // {
      //   id: 2,
      //   title: 'Optimizar consultas DB', 
      //   completed: false,
      //   category: 'laboral',
      //   customCategory: '',
      //   subtasks: [
      //     { id: 3, title: 'Indexar tablas principales', completed: false, timeSpent: 0 },
      //     { id: 4, title: 'Revisar queries N+1', completed: false, timeSpent: 0 }
      //   ],
      //   timeSpent: 0
      // }
    ]

  const initialPomodoro = getCurrentPomodoroFromCache() || {
    objective: '',
    taskId: null,
    subtaskIds: [],
    timer: 300, // 5 segundos para pruebas (normalmente 25 * 60)
    isRunning: false,
    mode: 'pomodoro' // pomodoro, shortBreak, longBreak
  }

  const [tasks, setTasks] = useState(initialTasks)
  const [currentPomodoro, setCurrentPomodoro] = useState(initialPomodoro)
  const [pomodoroCount, setPomodoroCount] = useState(getPomodoroCountFromCache())
  const [showDistractionModal, setShowDistractionModal] = useState(false)
  const [distractionModalShown, setDistractionModalShown] = useState([])

  // Guardar tareas en cache cuando cambien
  useEffect(() => {
    saveTasksToCache(tasks)
  }, [tasks])

  // Guardar pomodoro actual en cache cuando cambie
  useEffect(() => {
    saveCurrentPomodoroToCache(currentPomodoro)
  }, [currentPomodoro])

  // Guardar contador de pomodoros en cache cuando cambie
  useEffect(() => {
    savePomodoroCountToCache(pomodoroCount)
  }, [pomodoroCount])

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
