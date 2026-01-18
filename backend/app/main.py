"""
MyPomodoro Backend - FastAPI Application
Aplicación backend para gestión de tiempo tipo Pomodoro con FastAPI y Supabase
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks, subtasks, pomodoros, distractions, statistics
from app.config import settings
from app.database.supabase_client import get_supabase

app = FastAPI(
    title="MyPomodoro API",
    description="API REST para gestión de tiempo tipo Pomodoro",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tareas"])
app.include_router(subtasks.router, prefix="/api/v1/subtasks", tags=["Subtareas"])
app.include_router(pomodoros.router, prefix="/api/v1/pomodoros", tags=["Pomodoros"])
app.include_router(distractions.router, prefix="/api/v1/distractions", tags=["Distracciones"])
app.include_router(statistics.router, prefix="/api/v1/statistics", tags=["Estadísticas"])


@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "MyPomodoro API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servicio"""
    return {"status": "healthy"}


@app.get("/database-status")
async def database_status():
    """
    Endpoint para verificar la conexión a Supabase
    Intenta hacer una query simple para validar la conexión
    """
    try:
        supabase = get_supabase()
        
        # Intentar una query simple
        supabase.table("tasks").select("id").limit(1).execute()
        
        return {
            "status": "connected",
            "database": "supabase",
            "url": settings.SUPABASE_URL,
            "message": "Conexión a Supabase exitosa"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "disconnected",
                "error": str(e),
                "url": settings.SUPABASE_URL,
                "message": "No se puede conectar a Supabase"
            }
        )

