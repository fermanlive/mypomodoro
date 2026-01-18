"""
Router para endpoints de distracciones
"""

from fastapi import APIRouter, Query
from typing import List, Optional
from app.models.schemas import DistractionCreate, DistractionResponse
from app.services.distraction_service import DistractionService

router = APIRouter()


@router.post("/", response_model=DistractionResponse)
async def create_distraction(distraction: DistractionCreate):
    """Crear un nuevo registro de distracción"""
    return DistractionService.create_distraction(distraction)


@router.get("/", response_model=List[DistractionResponse])
async def get_distractions(
    user_id: Optional[str] = Query(None, description="ID del usuario para filtrar")
):
    """Obtener todas las distracciones"""
    return DistractionService.get_all_distractions(user_id=user_id)


@router.get("/pomodoro/{pomodoro_id}", response_model=List[DistractionResponse])
async def get_distractions_by_pomodoro(pomodoro_id: int):
    """Obtener todas las distracciones de un pomodoro"""
    return DistractionService.get_distractions_by_pomodoro_id(pomodoro_id)


@router.get("/{distraction_id}", response_model=DistractionResponse)
async def get_distraction(distraction_id: int):
    """Obtener una distracción por ID"""
    return DistractionService.get_distraction_by_id(distraction_id)
