# MyPomodoro

MyPomodoro es una herramienta personalizable para aplicar la técnica Pomodoro con un contador de tiempo, registro de tareas, alta configurabilidad y funcionalidades adicionales como automatización, integración con calendarios o notificaciones.

## 📋 Descripción del Proyecto

Este proyecto está dividido en dos partes principales:
- **Backend**: API REST desarrollada con FastAPI y Supabase
- **Frontend**: Aplicación web desarrollada con React y Vite

## 🚀 Configuración para Desarrollo

### Prerrequisitos

- Python 3.8+ (para el backend)
- Node.js 18+ y Yarn (para el frontend)
- Cuenta de Supabase (para la base de datos)

### 1. Configuración del Backend

1. **Navegar al directorio del backend**:
```bash
cd backend
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
```

3. **Activar entorno virtual**:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno**:
```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

6. **Editar el archivo `.env`** con tus credenciales de Supabase:
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-api-key-publica
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
DEBUG=True
```

7. **Configurar la base de datos**:
   - Ve a SQL Editor en tu proyecto de Supabase
   - Ejecuta el contenido de `docs/database/schema.sql`

8. **Ejecutar el servidor backend**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: `http://localhost:8000`
- Documentación API (Swagger): `http://localhost:8000/docs`
- Documentación alternativa (ReDoc): `http://localhost:8000/redoc`

### 2. Configuración del Frontend

1. **Navegar al directorio del frontend**:
```bash
cd frontend
```

2. **Instalar dependencias**:
```bash
yarn install
```

3. **Configurar variables de entorno** (opcional):
   - Crear archivo `.env` en el directorio `frontend/`:
```env
VITE_API_URL=http://localhost:8000
```

   **Nota**: Si no creas el archivo `.env`, el frontend usará `http://localhost:8000` por defecto.

4. **Ejecutar el servidor de desarrollo**:
```bash
yarn dev
```

El frontend estará disponible en: `http://localhost:5173`

## 🔗 Conexión entre Backend y Frontend

### Configuración Automática

El proyecto está configurado para que ambos servicios se comuniquen automáticamente en desarrollo:

1. **Backend (CORS)**:
   - El backend está configurado para aceptar peticiones desde `http://localhost:5173`
   - Esta configuración se encuentra en `backend/app/config.py` y se puede modificar en el archivo `.env` del backend

2. **Frontend (Proxy)**:
   - Vite está configurado con un proxy que redirige las peticiones `/api/*` al backend
   - Esta configuración se encuentra en `frontend/vite.config.js`
   - El proxy permite hacer peticiones sin problemas de CORS durante el desarrollo

3. **Servicio API**:
   - El frontend incluye un servicio API completo en `frontend/src/services/api.js`
   - Este servicio proporciona funciones para interactuar con todos los endpoints del backend:
     - `tasksAPI`: Gestión de tareas
     - `subtasksAPI`: Gestión de subtareas
     - `pomodorosAPI`: Gestión de pomodoros
     - `distractionsAPI`: Gestión de distracciones
     - `statisticsAPI`: Estadísticas

### Uso del Servicio API

Ejemplo de cómo usar el servicio API en tus componentes:

```javascript
import { tasksAPI } from './services/api'

// Obtener todas las tareas
const tasks = await tasksAPI.getAll()

// Crear una nueva tarea
const newTask = await tasksAPI.create({
  title: 'Mi nueva tarea',
  category: 'laboral',
  completed: false
})

// Actualizar una tarea
await tasksAPI.update(taskId, {
  title: 'Tarea actualizada',
  completed: true
})

// Eliminar una tarea
await tasksAPI.delete(taskId)
```

## 🏃 Ejecutar Ambos Servicios

### Opción 1: Terminales Separadas (Recomendado)

**Terminal 1 - Backend**:
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
yarn dev
```

### Opción 2: Scripts de Desarrollo

Puedes crear scripts personalizados en `package.json` para ejecutar ambos servicios simultáneamente (requiere herramientas como `concurrently`).

## 📁 Estructura del Proyecto

```
mypomodoro/
├── backend/
│   ├── app/
│   │   ├── main.py              # Aplicación FastAPI principal
│   │   ├── config.py             # Configuración (CORS, etc.)
│   │   ├── routers/              # Endpoints de la API
│   │   ├── services/             # Lógica de negocio
│   │   ├── models/               # Esquemas Pydantic
│   │   └── database/             # Cliente Supabase
│   ├── docs/                     # Documentación
│   ├── requirements.txt          # Dependencias Python
│   └── .env                      # Variables de entorno (no versionado)
│
└── frontend/
    ├── src/
    │   ├── components/           # Componentes React
    │   ├── services/
    │   │   └── api.js            # Cliente API para backend
    │   ├── App.jsx               # Componente principal
    │   └── main.jsx              # Punto de entrada
    ├── vite.config.js            # Configuración Vite (incluye proxy)
    ├── package.json              # Dependencias Node.js
    └── .env                      # Variables de entorno (opcional)
```

## 🔧 Configuración de Puertos

Por defecto:
- **Backend**: `http://localhost:8000`
- **Frontend**: `http://localhost:5173`

Si necesitas cambiar estos puertos:

### Cambiar puerto del Backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port TU_PUERTO
```

### Cambiar puerto del Frontend:
Editar `frontend/vite.config.js`:
```javascript
server: {
  port: TU_PUERTO,
  // ...
}
```

Y actualizar `CORS_ORIGINS` en el `.env` del backend para incluir el nuevo puerto.

## 🐛 Solución de Problemas

### Error de CORS

Si ves errores de CORS en la consola del navegador:
1. Verifica que `CORS_ORIGINS` en el `.env` del backend incluya `http://localhost:5173`
2. Reinicia el servidor backend después de cambiar el `.env`
3. Verifica que el proxy en `vite.config.js` esté configurado correctamente

### Error de conexión al backend

1. Verifica que el backend esté ejecutándose en `http://localhost:8000`
2. Prueba acceder directamente a `http://localhost:8000/docs` en tu navegador
3. Verifica que no haya un firewall bloqueando el puerto 8000
4. Revisa la consola del navegador para ver el error específico

### Variables de entorno no funcionan

1. En el frontend, las variables deben comenzar con `VITE_` para ser accesibles
2. Reinicia el servidor de desarrollo después de cambiar variables de entorno
3. Verifica que el archivo `.env` esté en el directorio correcto

## 📚 Documentación Adicional

- **Backend**: Ver `backend/README.md` para documentación completa de la API
- **Frontend**: Ver `frontend/README.md` para detalles del frontend
- **Base de datos**: Ver `backend/docs/database/schema.md` para el esquema de la BD

## 📝 Notas de Desarrollo

- El proxy de Vite solo funciona en desarrollo. Para producción, necesitarás configurar un servidor web (nginx, Apache, etc.) o usar variables de entorno para la URL del backend.
- Todos los tiempos se manejan en **segundos** en el backend.
- El frontend actualmente usa datos mock. Para usar el backend real, necesitarás integrar el servicio API en los componentes.

## 📄 Licencia

Ver archivo `LICENSE` para más detalles.
