import { useState } from 'react'
import './TaskList.css'

function TaskList({ tasks, onTasksChange, currentPomodoro, onCurrentPomodoroChange }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [editingTask, setEditingTask] = useState(null)
  const [expandedTasks, setExpandedTasks] = useState(new Set(tasks.map(t => t.id)))
  const [openMenuId, setOpenMenuId] = useState(null)

  const filteredTasks = tasks.filter(task =>
    task.title.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const toggleTaskExpanded = (taskId) => {
    setExpandedTasks(prev => {
      const newSet = new Set(prev)
      if (newSet.has(taskId)) {
        newSet.delete(taskId)
      } else {
        newSet.add(taskId)
      }
      return newSet
    })
  }

  const toggleTaskComplete = (taskId) => {
    const updatedTasks = tasks.map(task => {
      if (task.id === taskId) {
        return { ...task, completed: !task.completed }
      }
      return task
    })
    onTasksChange(updatedTasks)
  }

  const toggleSubtaskComplete = (taskId, subtaskId) => {
    const updatedTasks = tasks.map(task => {
      if (task.id === taskId) {
        const updatedSubtasks = task.subtasks.map(subtask => {
          if (subtask.id === subtaskId) {
            return { ...subtask, completed: !subtask.completed }
          }
          return subtask
        })
        const allSubtasksComplete = updatedSubtasks.every(st => st.completed)
        return {
          ...task,
          subtasks: updatedSubtasks,
          completed: allSubtasksComplete
        }
      }
      return task
    })
    onTasksChange(updatedTasks)
  }

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    if (hours > 0) {
      return `${hours}h ${minutes}m`
    }
    return `${minutes}m`
  }

  const getCompletedSubtasksCount = (task) => {
    return task.subtasks.filter(st => st.completed).length
  }

  const getTotalSubtasksCount = (task) => {
    return task.subtasks.length
  }

  const getProgressPercentage = (task) => {
    if (task.subtasks.length === 0) return task.completed ? 100 : 0
    const completed = getCompletedSubtasksCount(task)
    return (completed / task.subtasks.length) * 100
  }

  const handleSelectForPomodoro = (taskId, subtaskIds) => {
    onCurrentPomodoroChange({
      ...currentPomodoro,
      taskId,
      subtaskIds
    })
  }

  const handleAddTask = () => {
    const newTask = {
      id: Date.now(),
      title: 'Nueva tarea',
      completed: false,
      category: 'personal',
      customCategory: '',
      subtasks: [],
      timeSpent: 0
    }
    onTasksChange([...tasks, newTask])
    setEditingTask(newTask.id)
  }

  const handleCategoryChange = (taskId, newCategory) => {
    const updatedTasks = tasks.map(task => {
      if (task.id === taskId) {
        return {
          ...task,
          category: newCategory,
          customCategory: newCategory !== 'otro' ? '' : task.customCategory
        }
      }
      return task
    })
    onTasksChange(updatedTasks)
  }

  const handleCustomCategoryChange = (taskId, customCategory) => {
    const updatedTasks = tasks.map(task => {
      if (task.id === taskId) {
        return { ...task, customCategory }
      }
      return task
    })
    onTasksChange(updatedTasks)
  }


  const handleTaskTitleChange = (taskId, newTitle) => {
    const updatedTasks = tasks.map(task => {
      if (task.id === taskId) {
        return { ...task, title: newTitle }
      }
      return task
    })
    onTasksChange(updatedTasks)
  }

  const handleAddSubtask = (taskId) => {
    const updatedTasks = tasks.map(task => {
      if (task.id === taskId) {
        const newSubtask = {
          id: Date.now(),
          title: 'Nueva subtarea',
          completed: false,
          timeSpent: 0
        }
        return {
          ...task,
          subtasks: [...task.subtasks, newSubtask]
        }
      }
      return task
    })
    onTasksChange(updatedTasks)
  }

  const handleArchiveTask = (taskId) => {
    // Por ahora simplemente eliminamos la tarea
    // En una implementación real, podrías moverla a una lista de archivadas
    const updatedTasks = tasks.filter(task => task.id !== taskId)
    onTasksChange(updatedTasks)
    setOpenMenuId(null)
  }

  const handleDeleteTask = (taskId) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar esta tarea?')) {
      const updatedTasks = tasks.filter(task => task.id !== taskId)
      onTasksChange(updatedTasks)
      setOpenMenuId(null)
    }
  }

  const handleMenuToggle = (taskId, e) => {
    e.stopPropagation()
    setOpenMenuId(openMenuId === taskId ? null : taskId)
  }

  // Cerrar menú al hacer clic fuera
  const handleClickOutside = () => {
    setOpenMenuId(null)
  }

  return (
    <div className="task-list-container" onClick={handleClickOutside}>
      <div className="task-list-header">
        <h2 className="task-list-title">Tasks</h2>
        <div className="task-list-search">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Search tasks..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>
      </div>
      
      <div className="task-list-content">
        {filteredTasks.map(task => {
          const isExpanded = expandedTasks.has(task.id)
          const completedCount = getCompletedSubtasksCount(task)
          const totalCount = getTotalSubtasksCount(task)
          const progress = getProgressPercentage(task)
          const isSelected = currentPomodoro.taskId === task.id

          return (
            <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''} ${isSelected ? 'selected' : ''}`}>
              <div className="task-header">
                <div className="task-main">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => toggleTaskComplete(task.id)}
                    className="task-checkbox"
                  />
                  <div 
                    className="task-content"
                    onClick={() => toggleTaskExpanded(task.id)}
                  >
                    {editingTask === task.id ? (
                      <input
                        type="text"
                        value={task.title}
                        onChange={(e) => handleTaskTitleChange(task.id, e.target.value)}
                        onBlur={() => setEditingTask(null)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') setEditingTask(null)
                        }}
                        className="task-title-input"
                        autoFocus
                      />
                    ) : (
                      <span 
                        className="task-title"
                        onDoubleClick={() => setEditingTask(task.id)}
                      >
                        {task.title}
                      </span>
                    )}
                    {task.subtasks.length > 0 && (
                      <span className="task-progress-indicator">
                        {completedCount}/{totalCount}
                      </span>
                    )}
                  </div>
                </div>
                <div className="task-menu-container">
                  <button 
                    className="task-menu-btn" 
                    onClick={(e) => handleMenuToggle(task.id, e)}
                  >
                    ⋯
                  </button>
                  {openMenuId === task.id && (
                    <div 
                      className="task-menu-dropdown"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <button
                        className="task-menu-item"
                        onClick={(e) => {
                          e.stopPropagation()
                          handleArchiveTask(task.id)
                        }}
                      >
                        📦 Archivar
                      </button>
                      <button
                        className="task-menu-item delete"
                        onClick={(e) => {
                          e.stopPropagation()
                          handleDeleteTask(task.id)
                        }}
                      >
                        🗑️ Eliminar
                      </button>
                    </div>
                  )}
                </div>
              </div>

              {isExpanded && task.subtasks.length > 0 && (
                <div className="task-subtasks">
                  {task.subtasks.map(subtask => (
                    <div key={subtask.id} className="subtask-item">
                      <input
                        type="checkbox"
                        checked={subtask.completed}
                        onChange={() => toggleSubtaskComplete(task.id, subtask.id)}
                        className="subtask-checkbox"
                      />
                      <span className="subtask-title">{subtask.title}</span>
                      <span className="subtask-time">{formatTime(subtask.timeSpent)}</span>
                      <button
                        className="subtask-select-btn"
                        onClick={() => handleSelectForPomodoro(task.id, [subtask.id])}
                      >
                        Seleccionar
                      </button>
                    </div>
                  ))}
                  <button
                    className="add-subtask-btn"
                    onClick={() => handleAddSubtask(task.id)}
                  >
                    + Add Subtask
                  </button>
                  {task.subtasks.length > 1 && (
                    <button
                      className="select-all-subtasks-btn"
                      onClick={() => handleSelectForPomodoro(
                        task.id,
                        task.subtasks.map(st => st.id)
                      )}
                    >
                      Seleccionar todas
                    </button>
                  )}
                </div>
              )}

              {isExpanded && (
                <>
                  <div className="task-category-section">
                    <label className="task-category-label">Categoría:</label>
                    <select
                      value={task.category}
                      onChange={(e) => handleCategoryChange(task.id, e.target.value)}
                      className="task-category-select"
                    >
                      <option value="personal">Personal</option>
                      <option value="laboral">Laboral</option>
                      <option value="otro">Otro</option>
                    </select>
                    {task.category === 'otro' && (
                      <input
                        type="text"
                        value={task.customCategory || ''}
                        onChange={(e) => handleCustomCategoryChange(task.id, e.target.value)}
                        placeholder="Define el nombre de la categoría..."
                        className="task-custom-category-input"
                      />
                    )}
                  </div>
                  <div className="task-progress-bar">
                    <div
                      className="task-progress-fill"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                </>
              )}
            </div>
          )
        })}
      </div>

      <button className="add-task-btn" onClick={handleAddTask}>
        <span>+</span>
        Add Task
      </button>
    </div>
  )
}

export default TaskList
