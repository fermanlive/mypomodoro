/**
 * Servicio API para comunicarse con el backend
 */

import { getAuthToken, getUserId } from './auth'

// En desarrollo, usar ruta relativa para aprovechar el proxy de Vite
// En producción, usar la URL completa desde variables de entorno
const API_URL = import.meta.env.VITE_API_URL || '';

/**
 * Función auxiliar para hacer peticiones HTTP
 */
async function request(endpoint, options = {}) {
  // Si API_URL está vacío, usar ruta relativa (proxy de Vite)
  // Si API_URL tiene valor, usar URL completa (producción)
  const url = API_URL ? `${API_URL}${endpoint}` : endpoint;
  
  // Obtener token de autenticación
  const token = getAuthToken();
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Añadir token de autenticación si existe
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  if (config.body && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body);
  }

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Error desconocido' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    // Si la respuesta está vacía (204 No Content), retornar null
    if (response.status === 204) {
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Error en petición API:', error);
    throw error;
  }
}

/**
 * API de Tareas
 */
export const tasksAPI = {
  /**
   * Obtener todas las tareas
   */
  getAll: async (params = {}) => {
    const queryParams = new URLSearchParams();
    // Si no se especifica userId, usar el ID actual (autenticado o anónimo)
    const userId = params.userId || getUserId();
    queryParams.append('user_id', userId);
    if (params.search) queryParams.append('search', params.search);
    
    const queryString = queryParams.toString();
    return request(`/api/v1/tasks${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Obtener una tarea por ID
   */
  getById: async (taskId) => {
    return request(`/api/v1/tasks/${taskId}`);
  },

  /**
   * Crear una nueva tarea
   */
  create: async (taskData) => {
    // Asegurar que el user_id se envía
    const dataWithUserId = {
      ...taskData,
      user_id: taskData.user_id || getUserId()
    };
    return request('/api/v1/tasks', {
      method: 'POST',
      body: dataWithUserId,
    });
  },

  /**
   * Actualizar una tarea
   */
  update: async (taskId, taskData) => {
    return request(`/api/v1/tasks/${taskId}`, {
      method: 'PUT',
      body: taskData,
    });
  },

  /**
   * Eliminar una tarea
   */
  delete: async (taskId) => {
    return request(`/api/v1/tasks/${taskId}`, {
      method: 'DELETE',
    });
  },
};

/**
 * API de Subtareas
 */
export const subtasksAPI = {
  /**
   * Obtener todas las subtareas de una tarea
   */
  getByTaskId: async (taskId, userId = null) => {
    const actualUserId = userId || getUserId();
    return request(`/api/v1/subtasks/task/${taskId}?user_id=${actualUserId}`);
  },

  /**
   * Obtener una subtarea por ID
   */
  getById: async (subtaskId) => {
    return request(`/api/v1/subtasks/${subtaskId}`);
  },

  /**
   * Crear una nueva subtarea
   */
  create: async (subtaskData) => {
    const dataWithUserId = {
      ...subtaskData,
      user_id: subtaskData.user_id || getUserId()
    };
    return request('/api/v1/subtasks', {
      method: 'POST',
      body: dataWithUserId,
    });
  },

  /**
   * Actualizar una subtarea
   */
  update: async (subtaskId, subtaskData) => {
    return request(`/api/v1/subtasks/${subtaskId}`, {
      method: 'PUT',
      body: subtaskData,
    });
  },

  /**
   * Eliminar una subtarea
   */
  delete: async (subtaskId) => {
    return request(`/api/v1/subtasks/${subtaskId}`, {
      method: 'DELETE',
    });
  },
};

/**
 * API de Pomodoros
 */
export const pomodorosAPI = {
  /**
   * Obtener todos los pomodoros
   */
  getAll: async (params = {}) => {
    const queryParams = new URLSearchParams();
    const userId = params.userId || getUserId();
    queryParams.append('user_id', userId);
    if (params.taskId) queryParams.append('task_id', params.taskId);
    if (params.completed !== undefined) queryParams.append('completed', params.completed);
    
    const queryString = queryParams.toString();
    return request(`/api/v1/pomodoros${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Obtener un pomodoro por ID
   */
  getById: async (pomodoroId) => {
    return request(`/api/v1/pomodoros/${pomodoroId}`);
  },

  /**
   * Obtener conteo de pomodoros completados
   */
  getCount: async (params = {}) => {
    const queryParams = new URLSearchParams();
    const userId = params.userId || getUserId();
    queryParams.append('user_id', userId);
    
    const queryString = queryParams.toString();
    return request(`/api/v1/pomodoros/count${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Crear un nuevo pomodoro
   */
  create: async (pomodoroData) => {
    const dataWithUserId = {
      ...pomodoroData,
      user_id: pomodoroData.user_id || getUserId()
    };
    return request('/api/v1/pomodoros', {
      method: 'POST',
      body: dataWithUserId,
    });
  },

  /**
   * Actualizar un pomodoro
   */
  update: async (pomodoroId, pomodoroData) => {
    return request(`/api/v1/pomodoros/${pomodoroId}`, {
      method: 'PUT',
      body: pomodoroData,
    });
  },

  /**
   * Completar un pomodoro
   */
  complete: async (pomodoroId, actualDuration = null) => {
    return request('/api/v1/pomodoros/complete', {
      method: 'POST',
      body: {
        pomodoro_id: pomodoroId,
        actual_duration: actualDuration,
      },
    });
  },
};

/**
 * API de Distracciones
 */
export const distractionsAPI = {
  /**
   * Obtener todas las distracciones
   */
  getAll: async (params = {}) => {
    const queryParams = new URLSearchParams();
    const userId = params.userId || getUserId();
    queryParams.append('user_id', userId);
    
    const queryString = queryParams.toString();
    return request(`/api/v1/distractions${queryString ? `?${queryString}` : ''}`);
  },

  /**
   * Obtener distracciones de un pomodoro
   */
  getByPomodoroId: async (pomodoroId) => {
    return request(`/api/v1/distractions/pomodoro/${pomodoroId}`);
  },

  /**
   * Obtener una distracción por ID
   */
  getById: async (distractionId) => {
    return request(`/api/v1/distractions/${distractionId}`);
  },

  /**
   * Crear un registro de distracción
   */
  create: async (distractionData) => {
    const dataWithUserId = {
      ...distractionData,
      user_id: distractionData.user_id || getUserId()
    };
    return request('/api/v1/distractions', {
      method: 'POST',
      body: dataWithUserId,
    });
  },
};

/**
 * API de Estadísticas
 */
export const statisticsAPI = {
  /**
   * Obtener estadísticas generales
   */
  getAll: async (params = {}) => {
    const queryParams = new URLSearchParams();
    const userId = params.userId || getUserId();
    queryParams.append('user_id', userId);
    
    const queryString = queryParams.toString();
    return request(`/api/v1/statistics${queryString ? `?${queryString}` : ''}`);
  },
};
