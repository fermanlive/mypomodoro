import './Header.css'

function Header() {
  return (
    <header className="header">
      <div className="header-left">
        <span className="header-icon">🤖</span>
        <h1 className="header-title">DevPomodoro</h1>
      </div>
      <div className="header-right">
        <button className="header-btn">
          <span>📊</span>
          Report
        </button>
        <button className="header-btn">
          <span>⚙️</span>
          Settings
        </button>
        <button className="header-btn">
          <span>👤</span>
          Sign In
        </button>
        <button className="header-btn icon-only">⋯</button>
      </div>
    </header>
  )
}

export default Header
