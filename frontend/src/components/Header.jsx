import { isAuthenticated, getCurrentUser, clearSession, setSession } from '../services/auth'
import './Header.css'

function Header() {
  const user = getCurrentUser()
  
  const handleAuthToggle = () => {
    if (user.isAuthenticated) {
      // Logout
      clearSession()
      window.location.reload()
    } else {
      // Login (simulado - en producción sería un modal de login)
      const userId = prompt('Ingresa tu ID de usuario:')
      const token = prompt('Ingresa tu token de autenticación:')
      if (userId && token) {
        setSession(token, userId)
        window.location.reload()
      }
    }
  }

  return (
    <header className="header">
      <div className="header-left">
        <span className="header-icon">🤖</span>
        <h1 className="header-title">DevPomodoro</h1>
      </div>
      <div className="header-right" style={{display: "none"}}>
        <button className="header-btn">
          <span>📊</span>
          Report
        </button>
        <button className="header-btn">
          <span>⚙️</span>
          Settings
        </button>
        <button className="header-btn" onClick={handleAuthToggle}>
          <span>{user.isAuthenticated ? '👤' : '🔓'}</span>
          {user.isAuthenticated ? 'Sign Out' : 'Sign In'}
        </button>
        {user.isAuthenticated && (
          <button className="header-btn" title={`User: ${user.id}`}>
            <span>✓</span>
            Logged In
          </button>
        )}
        {!user.isAuthenticated && (
          <button className="header-btn" title="Not authenticated - using cache" style={{opacity: 0.6}}>
            <span>⚠️</span>
            Offline
          </button>
        )}
        <button className="header-btn icon-only">⋯</button>
      </div>
    </header>
  )
}

export default Header
