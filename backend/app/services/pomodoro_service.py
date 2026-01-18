"""
Servicio para operaciones con pomodoros
"""

from typing import List, Optional
from app.database.supabase_client import get_supabase
from app.models.schemas import (
    PomodoroCreate, PomodoroUpdate, PomodoroResponse, 
    PomodoroComplete
)
from fastapi import HTTPException, status
from datetime import datetime
from app.services.subtask_service import SubtaskService
from app.services.task_service import TaskService


class PomodoroService:
    """Servicio para gestionar pomodoros"""
    
    @staticmethod
    def create_pomodoro(pomodoro: PomodoroCreate) -> PomodoroResponse:
        """Crear un nuevo pomodoro"""
        supabase = get_supabase()
        
        # Verificar que la tarea existe si se proporciona
        if pomodoro.task_id:
            TaskService.get_task_by_id(pomodoro.task_id)
        
        pomodoro_data = pomodoro.model_dump(exclude_unset=True)
        
        # Establecer duración por defecto según el modo
        if not pomodoro_data.get("duration"):
            mode_durations = {
                "pomodoro": 1500,  # 25 minutos
                "shortBreak": 300,  # 5 minutos
                "longBreak": 900   # 15 minutos
            }
            pomodoro_data["duration"] = mode_durations.get(pomodoro_data.get("mode", "pomodoro"), 1500)
        
        try:
            result = supabase.table("pomodoros").insert(pomodoro_data).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear el pomodoro"
                )
            
            return PomodoroResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el pomodoro: {str(e)}"
            )
    
    @staticmethod
    def get_pomodoro_by_id(pomodoro_id: int) -> PomodoroResponse:
        """Obtener un pomodoro por ID"""
        supabase = get_supabase()
        
        try:
            result = supabase.table("pomodoros").select("*").eq("id", pomodoro_id).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Pomodoro con ID {pomodoro_id} no encontrado"
                )
            
            return PomodoroResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener el pomodoro: {str(e)}"
            )
    
    @staticmethod
    def get_all_pomodoros(user_id: Optional[str] = None, completed: Optional[bool] = None) -> List[PomodoroResponse]:
        """Obtener todos los pomodoros, opcionalmente filtrados"""
        supabase = get_supabase()
        
        try:
            query = supabase.table("pomodoros").select("*")
            
            if user_id:
                query = query.eq("user_id", user_id)
            
            if completed is not None:
                query = query.eq("completed", completed)
            
            result = query.order("created_at", desc=True).execute()
            
            return [PomodoroResponse(**p) for p in result.data] if result.data else []
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener los pomodoros: {str(e)}"
            )
    
    @staticmethod
    def update_pomodoro(pomodoro_id: int, pomodoro_update: PomodoroUpdate) -> PomodoroResponse:
        """Actualizar un pomodoro (útil para actualizar el estado mientras corre)"""
        supabase = get_supabase()
        
        # Verificar que el pomodoro existe
        PomodoroService.get_pomodoro_by_id(pomodoro_id)
        
        update_data = pomodoro_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return PomodoroService.get_pomodoro_by_id(pomodoro_id)
        
        try:
            result = supabase.table("pomodoros").update(update_data).eq("id", pomodoro_id).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al actualizar el pomodoro"
                )
            
            return PomodoroResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar el pomodoro: {str(e)}"
            )
    
    @staticmethod
    def complete_pomodoro(pomodoro_complete: PomodoroComplete) -> PomodoroResponse:
        """Completar un pomodoro y actualizar tiempos de subtareas"""
        supabase = get_supabase()
        
        # Obtener el pomodoro
        pomodoro = PomodoroService.get_pomodoro_by_id(pomodoro_complete.pomodoro_id)
        
        # Solo actualizar tiempos si es un pomodoro (no un break)
        if pomodoro.mode == "pomodoro" and pomodoro.subtask_ids:
            # Duración a sumar (por defecto 25 minutos = 1500 segundos)
            duration_to_add = pomodoro_complete.actual_duration or pomodoro.duration or 1500
            
            # Actualizar tiempo de cada subtarea
            for subtask_id in pomodoro.subtask_ids:
                subtask = SubtaskService.get_subtask_by_id(subtask_id)
                new_time = subtask.time_spent + duration_to_add
                SubtaskService.update_subtask(subtask_id, {"time_spent": new_time})
        
        # Marcar pomodoro como completado
        update_data = {
            "completed": True,
            "completed_at": datetime.utcnow().isoformat()
        }
        
        if pomodoro_complete.actual_duration:
            update_data["duration"] = pomodoro_complete.actual_duration
        
        try:
            result = supabase.table("pomodoros").update(update_data).eq("id", pomodoro_complete.pomodoro_id).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al completar el pomodoro"
                )
            
            return PomodoroResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al completar el pomodoro: {str(e)}"
            )
    
    @staticmethod
    def get_pomodoro_count(user_id: Optional[str] = None) -> int:
        """Obtener el conteo total de pomodoros completados"""
        supabase = get_supabase()
        
        try:
            query = supabase.table("pomodoros").select("id", count="exact")
            query = query.eq("completed", True).eq("mode", "pomodoro")
            
            if user_id:
                query = query.eq("user_id", user_id)
            
            result = query.execute()
            
            # Supabase devuelve el count en los headers o en la respuesta
            return result.count if hasattr(result, 'count') and result.count else len(result.data or [])
        except Exception as e:
            # Fallback: contar manualmente
            pomodoros = PomodoroService.get_all_pomodoros(user_id=user_id, completed=True)
            return len([p for p in pomodoros if p.mode == "pomodoro"])
