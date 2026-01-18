"""
Router para endpoints de subtareas
"""

from fastapi import APIRouter
from typing import List
from app.models.schemas import SubtaskCreate, SubtaskUpdate, SubtaskResponse
from app.services.subtask_service import SubtaskService

router = APIRouter()


@router.post("/", response_model=SubtaskResponse)
async def create_subtask(subtask: SubtaskCreate):
    """Crear una nueva subtarea"""
    return SubtaskService.create_subtask(subtask)


@router.get("/task/{task_id}", response_model=List[SubtaskResponse])
async def get_subtasks_by_task(task_id: int):
    """Obtener todas las subtareas de una tarea"""
    return SubtaskService.get_subtasks_by_task_id(task_id)


@router.get("/{subtask_id}", response_model=SubtaskResponse)
async def get_subtask(subtask_id: int):
    """Obtener una subtarea por ID"""
    return SubtaskService.get_subtask_by_id(subtask_id)


@router.put("/{subtask_id}", response_model=SubtaskResponse)
async def update_subtask(subtask_id: int, subtask_update: SubtaskUpdate):
    """Actualizar una subtarea"""
    return SubtaskService.update_subtask(subtask_id, subtask_update)


@router.delete("/{subtask_id}")
async def delete_subtask(subtask_id: int):
    """Eliminar una subtarea"""
    SubtaskService.delete_subtask(subtask_id)
    return {"message": "Subtarea eliminada correctamente"}
