"""
Router para endpoints de tareas
"""

from fastapi import APIRouter, Query, HTTPException, status
from typing import List, Optional
from app.models.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """Crear una nueva tarea"""
    return TaskService.create_task(task)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    user_id: Optional[str] = Query(None, description="ID del usuario para filtrar"),
    search: Optional[str] = Query(None, description="Búsqueda por título")
):
    """Obtener todas las tareas con filtros opcionales"""
    return TaskService.get_all_tasks(user_id=user_id, search=search)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    """Obtener una tarea por ID"""
    return TaskService.get_task_by_id(task_id)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Actualizar una tarea"""
    return TaskService.update_task(task_id, task_update)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    """Eliminar una tarea"""
    TaskService.delete_task(task_id)
    return None
