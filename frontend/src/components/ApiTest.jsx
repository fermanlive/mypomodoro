import { useState } from 'react'
import { tasksAPI } from '../services/api'

function ApiTest() {
  const [status, setStatus] = useState('idle')
  const [message, setMessage] = useState('')
  const [data, setData] = useState(null)

  const testConnection = async () => {
    setStatus('loading')
    setMessage('Probando conexión...')
    
    try {
      // Probar obtener tareas
      const tasks = await tasksAPI.getAll()
      setData(tasks)
      setStatus('success')
      setMessage(`✅ Conexión exitosa! Se recibieron ${Array.isArray(tasks) ? tasks.length : 0} tareas`)
    } catch (error) {
      setStatus('error')
      setMessage(`❌ Error: ${error.message}`)
      console.error('Error de conexión:', error)
    }
  }

  return (
    <div style={{ 
      padding: '20px', 
      margin: '20px', 
      border: '1px solid #333', 
      borderRadius: '8px',
      backgroundColor: '#1a1a1a'
    }}>
      <h3 style={{ color: '#fff', marginBottom: '10px' }}>Prueba de Conexión API</h3>
      <button 
        onClick={testConnection}
        disabled={status === 'loading'}
        style={{
          padding: '10px 20px',
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: status === 'loading' ? 'not-allowed' : 'pointer',
          marginBottom: '10px'
        }}
      >
        {status === 'loading' ? 'Probando...' : 'Probar Conexión'}
      </button>
      
      {message && (
        <div style={{ 
          marginTop: '10px', 
          padding: '10px',
          backgroundColor: status === 'error' ? '#ff4444' : status === 'success' ? '#44ff44' : '#444',
          borderRadius: '4px',
          color: '#fff'
        }}>
          {message}
        </div>
      )}

      {data && (
        <pre style={{ 
          marginTop: '10px', 
          padding: '10px',
          backgroundColor: '#2a2a2a',
          borderRadius: '4px',
          color: '#fff',
          overflow: 'auto',
          maxHeight: '200px'
        }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  )
}

export default ApiTest
