"""
Servicio para operaciones con subtareas
"""

from typing import List
from app.database.supabase_client import get_supabase
from app.models.schemas import SubtaskCreate, SubtaskUpdate, SubtaskResponse
from fastapi import HTTPException, status
from app.services.task_service import TaskService


class SubtaskService:
    """Servicio para gestionar subtareas"""
    
    @staticmethod
    def create_subtask(subtask: SubtaskCreate) -> SubtaskResponse:
        """Crear una nueva subtarea"""
        supabase = get_supabase()
        
        # Verificar que la tarea existe
        TaskService.get_task_by_id(subtask.task_id)
        
        subtask_data = subtask.model_dump(exclude_unset=True)
        
        try:
            result = supabase.table("subtasks").insert(subtask_data).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear la subtarea"
                )
            
            return SubtaskResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la subtarea: {str(e)}"
            )
    
    @staticmethod
    def get_subtask_by_id(subtask_id: int) -> SubtaskResponse:
        """Obtener una subtarea por ID"""
        supabase = get_supabase()
        
        try:
            result = supabase.table("subtasks").select("*").eq("id", subtask_id).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Subtarea con ID {subtask_id} no encontrada"
                )
            
            return SubtaskResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la subtarea: {str(e)}"
            )
    
    @staticmethod
    def get_subtasks_by_task_id(task_id: int) -> List[SubtaskResponse]:
        """Obtener todas las subtareas de una tarea"""
        supabase = get_supabase()
        
        # Verificar que la tarea existe
        TaskService.get_task_by_id(task_id)
        
        try:
            result = supabase.table("subtasks").select("*").eq("task_id", task_id).order("created_at").execute()
            
            return [SubtaskResponse(**st) for st in result.data] if result.data else []
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener las subtareas: {str(e)}"
            )
    
    @staticmethod
    def update_subtask(subtask_id: int, subtask_update: SubtaskUpdate) -> SubtaskResponse:
        """Actualizar una subtarea"""
        supabase = get_supabase()
        
        # Verificar que la subtarea existe
        SubtaskService.get_subtask_by_id(subtask_id)
        
        update_data = subtask_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return SubtaskService.get_subtask_by_id(subtask_id)
        
        try:
            result = supabase.table("subtasks").update(update_data).eq("id", subtask_id).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al actualizar la subtarea"
                )
            
            return SubtaskResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar la subtarea: {str(e)}"
            )
    
    @staticmethod
    def delete_subtask(subtask_id: int) -> bool:
        """Eliminar una subtarea"""
        supabase = get_supabase()
        
        # Verificar que la subtarea existe
        SubtaskService.get_subtask_by_id(subtask_id)
        
        try:
            result = supabase.table("subtasks").delete().eq("id", subtask_id).execute()
            
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar la subtarea: {str(e)}"
            )
