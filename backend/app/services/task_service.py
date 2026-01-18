"""
Servicio para operaciones con tareas
"""

from typing import List, Optional
from app.database.supabase_client import get_supabase
from app.models.schemas import TaskCreate, TaskUpdate, TaskResponse, SubtaskResponse
from fastapi import HTTPException, status


class TaskService:
    """Servicio para gestionar tareas"""
    
    @staticmethod
    def create_task(task: TaskCreate) -> TaskResponse:
        """Crear una nueva tarea"""
        supabase = get_supabase()
        
        task_data = task.model_dump(exclude_unset=True, exclude={"subtasks"})
        
        try:
            result = supabase.table("tasks").insert(task_data).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear la tarea"
                )
            
            return TaskService.get_task_by_id(result.data[0]["id"])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la tarea: {str(e)}"
            )
    
    @staticmethod
    def get_task_by_id(task_id: int) -> TaskResponse:
        """Obtener una tarea por ID con sus subtareas"""
        supabase = get_supabase()
        
        try:
            # Obtener la tarea
            task_result = supabase.table("tasks").select("*").eq("id", task_id).execute()
            
            if not task_result.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tarea con ID {task_id} no encontrada"
                )
            
            task_data = task_result.data[0]
            
            # Obtener subtareas
            subtasks_result = supabase.table("subtasks").select("*").eq("task_id", task_id).order("created_at").execute()
            subtasks = [SubtaskResponse(**st) for st in subtasks_result.data] if subtasks_result.data else []
            
            task_data["subtasks"] = subtasks
            
            return TaskResponse(**task_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la tarea: {str(e)}"
            )
    
    @staticmethod
    def get_all_tasks(user_id: Optional[str] = None, search: Optional[str] = None) -> List[TaskResponse]:
        """Obtener todas las tareas, opcionalmente filtradas por user_id y búsqueda"""
        supabase = get_supabase()
        
        try:
            query = supabase.table("tasks").select("*")
            
            if user_id:
                query = query.eq("user_id", user_id)
            
            if search:
                query = query.ilike("title", f"%{search}%")
            
            result = query.order("created_at", desc=True).execute()
            
            tasks = []
            if result.data:
                # Para cada tarea, obtener sus subtareas
                for task_data in result.data:
                    subtasks_result = supabase.table("subtasks").select("*").eq("task_id", task_data["id"]).order("created_at").execute()
                    subtasks = [SubtaskResponse(**st) for st in subtasks_result.data] if subtasks_result.data else []
                    task_data["subtasks"] = subtasks
                    tasks.append(TaskResponse(**task_data))
            
            return tasks
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener las tareas: {str(e)}"
            )
    
    @staticmethod
    def update_task(task_id: int, task_update: TaskUpdate) -> TaskResponse:
        """Actualizar una tarea"""
        supabase = get_supabase()
        
        # Verificar que la tarea existe
        TaskService.get_task_by_id(task_id)
        
        update_data = task_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return TaskService.get_task_by_id(task_id)
        
        try:
            result = supabase.table("tasks").update(update_data).eq("id", task_id).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al actualizar la tarea"
                )
            
            return TaskService.get_task_by_id(task_id)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar la tarea: {str(e)}"
            )
    
    @staticmethod
    def delete_task(task_id: int) -> bool:
        """Eliminar una tarea (las subtareas se eliminan en cascada)"""
        supabase = get_supabase()
        
        # Verificar que la tarea existe
        TaskService.get_task_by_id(task_id)
        
        try:
            result = supabase.table("tasks").delete().eq("id", task_id).execute()
            
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar la tarea: {str(e)}"
            )
