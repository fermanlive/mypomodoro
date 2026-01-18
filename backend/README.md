# MyPomodoro Backend

Backend API REST para la aplicación MyPomodoro, desarrollado con FastAPI y Supabase.

## 📋 Descripción

API backend completa que implementa todas las funcionalidades del frontend MyPomodoro:
- Gestión de tareas y subtareas
- Sistema de Pomodoro Timer
- Registro de distracciones
- Estadísticas y reportes

## 🚀 Instalación Rápida

Para una guía completa y detallada paso a paso, consulta: **[📦 Guía de Instalación Completa](docs/INSTALLATION.md)**

### Resumen rápido:

1. **Crear entorno virtual**:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**:
```bash
copy env.example .env  # Windows
# cp env.example .env  # Linux/Mac
# Editar .env con tus credenciales de Supabase
```

4. **Ejecutar el schema SQL en Supabase**:
   - Ir a SQL Editor en Supabase
   - Ejecutar `docs/database/schema.sql`

5. **Ejecutar el servidor**:
```bash
uvicorn app.main:app --reload
```

## ⚙️ Configuración

### Variables de entorno (.env)

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-api-key-publica
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
DEBUG=True
```

### Configurar Supabase

1. **Obtener credenciales**:
   - Ve a tu proyecto en Supabase
   - Settings → API
   - Copia `URL` y `anon public` key

2. **Crear las tablas**:
   - Ve a SQL Editor en Supabase
   - Copia y ejecuta el contenido de `database/schema.sql`

## 🏃 Ejecución

### Modo desarrollo

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Modo producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación API

Una vez ejecutando la aplicación, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🗂️ Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación FastAPI principal
│   ├── config.py               # Configuración de la app
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Esquemas Pydantic
│   ├── database/
│   │   ├── __init__.py
│   │   └── supabase_client.py  # Cliente Supabase
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py     # Lógica de negocio para tareas
│   │   ├── subtask_service.py  # Lógica de negocio para subtareas
│   │   ├── pomodoro_service.py # Lógica de negocio para pomodoros
│   │   └── distraction_service.py # Lógica de negocio para distracciones
│   └── routers/
│       ├── __init__.py
│       ├── tasks.py            # Endpoints de tareas
│       ├── subtasks.py         # Endpoints de subtareas
│       ├── pomodoros.py        # Endpoints de pomodoros
│       ├── distractions.py     # Endpoints de distracciones
│       └── statistics.py       # Endpoints de estadísticas
├── database/
│   └── schema.sql              # Esquema de base de datos
├── .env.example                # Ejemplo de variables de entorno
├── requirements.txt            # Dependencias Python
└── README.md                   # Este archivo
```

## 🔌 Endpoints Principales

### Tareas (`/api/v1/tasks`)
- `POST /` - Crear tarea
- `GET /` - Listar tareas (con filtros opcionales)
- `GET /{task_id}` - Obtener tarea por ID
- `PUT /{task_id}` - Actualizar tarea
- `DELETE /{task_id}` - Eliminar tarea

### Subtareas (`/api/v1/subtasks`)
- `POST /` - Crear subtarea
- `GET /task/{task_id}` - Listar subtareas de una tarea
- `GET /{subtask_id}` - Obtener subtarea por ID
- `PUT /{subtask_id}` - Actualizar subtarea
- `DELETE /{subtask_id}` - Eliminar subtarea

### Pomodoros (`/api/v1/pomodoros`)
- `POST /` - Crear pomodoro
- `GET /` - Listar pomodoros (con filtros opcionales)
- `GET /count` - Obtener conteo de pomodoros completados
- `GET /{pomodoro_id}` - Obtener pomodoro por ID
- `PUT /{pomodoro_id}` - Actualizar pomodoro
- `POST /complete` - Completar pomodoro y actualizar tiempos

### Distracciones (`/api/v1/distractions`)
- `POST /` - Crear registro de distracción
- `GET /` - Listar distracciones
- `GET /pomodoro/{pomodoro_id}` - Distracciones de un pomodoro
- `GET /{distraction_id}` - Obtener distracción por ID

### Estadísticas (`/api/v1/statistics`)
- `GET /` - Obtener estadísticas generales

## 🔧 Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para Python
- **Supabase**: Backend as a Service (PostgreSQL + API REST)
- **Pydantic**: Validación de datos con Python
- **Uvicorn**: Servidor ASGI para FastAPI

## 📝 Notas

- Todos los tiempos se manejan en **segundos**
- Los IDs son auto-incrementales (BIGSERIAL en PostgreSQL)
- Las relaciones entre tablas usan claves foráneas con CASCADE donde corresponde
- Los triggers en la BD actualizan automáticamente `time_spent` de tareas y `completed` cuando cambian las subtareas

## 🐛 Troubleshooting

### Error de conexión a Supabase
- Verifica que `SUPABASE_URL` y `SUPABASE_KEY` estén correctos en `.env`
- Asegúrate de que el proyecto de Supabase esté activo

### Error al ejecutar SQL
- Verifica que tengas permisos en el proyecto de Supabase
- Asegúrate de ejecutar el script completo desde `database/schema.sql`

### Errores de CORS
- Verifica que `CORS_ORIGINS` en `.env` incluya la URL del frontend
- Asegúrate de reiniciar el servidor después de cambiar `.env`

## 🧪 Tests

El proyecto incluye una suite completa de tests unitarios usando pytest.

### Ejecutar tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Un archivo específico
pytest tests/test_task_service.py
```

Para más información sobre los tests, consulta: **[📚 Documentación de Tests](tests/README.md)**

## 📄 Licencia

Este proyecto es parte de MyPomodoro.
