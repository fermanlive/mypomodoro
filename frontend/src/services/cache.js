/**
 * Servicio de Almacenamiento Local (Cache)
 * Gestiona el almacenamiento de datos en localStorage cuando no hay sesión
 */

const TASKS_CACHE_KEY = 'pomodoro_tasks_cache';
const POMODORO_COUNT_CACHE_KEY = 'pomodoro_count_cache';
const CURRENT_POMODORO_CACHE_KEY = 'current_pomodoro_cache';

/**
 * Guardar tareas en caché local
 */
export function saveTasksToCache(tasks) {
  try {
    localStorage.setItem(TASKS_CACHE_KEY, JSON.stringify(tasks));
  } catch (error) {
    console.error('Error guardando tareas en caché:', error);
  }
}

/**
 * Obtener tareas del caché local
 */
export function getTasksFromCache() {
  try {
    const cached = localStorage.getItem(TASKS_CACHE_KEY);
    return cached ? JSON.parse(cached) : [];
  } catch (error) {
    console.error('Error obteniendo tareas del caché:', error);
    return [];
  }
}

/**
 * Guardar contador de pomodoros en caché
 */
export function savePomodoroCountToCache(count) {
  try {
    localStorage.setItem(POMODORO_COUNT_CACHE_KEY, count.toString());
  } catch (error) {
    console.error('Error guardando contador en caché:', error);
  }
}

/**
 * Obtener contador de pomodoros del caché
 */
export function getPomodoroCountFromCache() {
  try {
    const cached = localStorage.getItem(POMODORO_COUNT_CACHE_KEY);
    return cached ? parseInt(cached) : 0;
  } catch (error) {
    console.error('Error obteniendo contador del caché:', error);
    return 0;
  }
}

/**
 * Guardar pomodoro actual en caché
 */
export function saveCurrentPomodoroToCache(pomodoro) {
  try {
    localStorage.setItem(CURRENT_POMODORO_CACHE_KEY, JSON.stringify(pomodoro));
  } catch (error) {
    console.error('Error guardando pomodoro actual en caché:', error);
  }
}

/**
 * Obtener pomodoro actual del caché
 */
export function getCurrentPomodoroFromCache() {
  try {
    const cached = localStorage.getItem(CURRENT_POMODORO_CACHE_KEY);
    return cached ? JSON.parse(cached) : null;
  } catch (error) {
    console.error('Error obteniendo pomodoro actual del caché:', error);
    return null;
  }
}

/**
 * Limpiar todo el caché
 */
export function clearCache() {
  try {
    localStorage.removeItem(TASKS_CACHE_KEY);
    localStorage.removeItem(POMODORO_COUNT_CACHE_KEY);
    localStorage.removeItem(CURRENT_POMODORO_CACHE_KEY);
  } catch (error) {
    console.error('Error limpiando caché:', error);
  }
}
