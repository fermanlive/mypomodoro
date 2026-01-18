"""
Router para endpoints de pomodoros
"""

from fastapi import APIRouter, Query
from typing import List, Optional
from app.models.schemas import (
    PomodoroCreate, PomodoroUpdate, PomodoroResponse, PomodoroComplete
)
from app.services.pomodoro_service import PomodoroService

router = APIRouter()


@router.post("/", response_model=PomodoroResponse)
async def create_pomodoro(pomodoro: PomodoroCreate):
    """Crear un nuevo pomodoro"""
    return PomodoroService.create_pomodoro(pomodoro)


@router.get("/", response_model=List[PomodoroResponse])
async def get_pomodoros(
    user_id: Optional[str] = Query(None, description="ID del usuario para filtrar"),
    completed: Optional[bool] = Query(None, description="Filtrar por estado de completitud")
):
    """Obtener todos los pomodoros con filtros opcionales"""
    return PomodoroService.get_all_pomodoros(user_id=user_id, completed=completed)


@router.get("/count", response_model=dict)
async def get_pomodoro_count(user_id: Optional[str] = Query(None)):
    """Obtener el conteo total de pomodoros completados"""
    count = PomodoroService.get_pomodoro_count(user_id=user_id)
    return {"count": count}


@router.get("/{pomodoro_id}", response_model=PomodoroResponse)
async def get_pomodoro(pomodoro_id: int):
    """Obtener un pomodoro por ID"""
    return PomodoroService.get_pomodoro_by_id(pomodoro_id)


@router.put("/{pomodoro_id}", response_model=PomodoroResponse)
async def update_pomodoro(pomodoro_id: int, pomodoro_update: PomodoroUpdate):
    """Actualizar un pomodoro (estado, objetivo, etc.)"""
    return PomodoroService.update_pomodoro(pomodoro_id, pomodoro_update)


@router.post("/complete", response_model=PomodoroResponse)
async def complete_pomodoro(pomodoro_complete: PomodoroComplete):
    """Completar un pomodoro y actualizar tiempos de subtareas"""
    return PomodoroService.complete_pomodoro(pomodoro_complete)
