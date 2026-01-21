/**
 * Servicio de Autenticación
 * Gestiona el estado de autenticación del usuario
 */

const ANONYMOUS_USER_ID = '00000000-0000-0000-0000-000000000000';
const AUTH_TOKEN_KEY = 'auth_token';
const USER_ID_KEY = 'user_id';

/**
 * Verificar si el usuario tiene sesión activa
 */
export function isAuthenticated() {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  return !!token;
}

/**
 * Obtener el ID del usuario actual
 * Si no hay sesión, retorna el ID anónimo
 */
export function getUserId() {
  if (isAuthenticated()) {
    return localStorage.getItem(USER_ID_KEY);
  }
  return ANONYMOUS_USER_ID;
}

/**
 * Obtener el token de autenticación
 */
export function getAuthToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

/**
 * Establecer sesión (login)
 */
export function setSession(token, userId) {
  localStorage.setItem(AUTH_TOKEN_KEY, token);
  localStorage.setItem(USER_ID_KEY, userId);
}

/**
 * Cerrar sesión (logout)
 */
export function clearSession() {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  localStorage.removeItem(USER_ID_KEY);
}

/**
 * Obtener datos del usuario actual
 */
export function getCurrentUser() {
  if (isAuthenticated()) {
    return {
      id: localStorage.getItem(USER_ID_KEY),
      isAuthenticated: true
    };
  }
  return {
    id: ANONYMOUS_USER_ID,
    isAuthenticated: false
  };
}
