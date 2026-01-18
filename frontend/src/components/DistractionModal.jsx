import { useState } from 'react'
import './DistractionModal.css'

function DistractionModal({ onClose }) {
  const [distractions, setDistractions] = useState(false)
  const [phoneUsed, setPhoneUsed] = useState(false)

  const handleSubmit = () => {
    // Aquí se podría enviar la data a un backend
    console.log('Distracciones:', distractions)
    console.log('Celular usado:', phoneUsed)
    onClose()
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2 className="modal-title">Reflexión del Pomodoro</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        
        <div className="modal-body">
          <div className="modal-question">
            <p className="question-text">
              ¿El anterior pomodoro tuviste distracciones?
            </p>
            <div className="question-buttons">
              <button
                className={`answer-btn ${distractions === true ? 'selected yes' : ''}`}
                onClick={() => setDistractions(true)}
              >
                Sí
              </button>
              <button
                className={`answer-btn ${distractions === false ? 'selected no' : ''}`}
                onClick={() => setDistractions(false)}
              >
                No
              </button>
            </div>
          </div>

          <div className="modal-question">
            <p className="question-text">
              ¿Usaste el celular en el último pomodoro?
            </p>
            <div className="question-buttons">
              <button
                className={`answer-btn ${phoneUsed === true ? 'selected yes' : ''}`}
                onClick={() => setPhoneUsed(true)}
              >
                Sí
              </button>
              <button
                className={`answer-btn ${phoneUsed === false ? 'selected no' : ''}`}
                onClick={() => setPhoneUsed(false)}
              >
                No
              </button>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="modal-submit-btn" onClick={handleSubmit}>
            Guardar
          </button>
        </div>
      </div>
    </div>
  )
}

export default DistractionModal
