"""
Servicio para operaciones con distracciones
"""

from typing import List
from app.database.supabase_client import get_supabase
from app.models.schemas import DistractionCreate, DistractionResponse
from fastapi import HTTPException, status
from app.services.pomodoro_service import PomodoroService


class DistractionService:
    """Servicio para gestionar distracciones"""
    
    @staticmethod
    def create_distraction(distraction: DistractionCreate) -> DistractionResponse:
        """Crear un nuevo registro de distracción"""
        supabase = get_supabase()
        
        # Verificar que el pomodoro existe
        PomodoroService.get_pomodoro_by_id(distraction.pomodoro_id)
        
        distraction_data = distraction.model_dump(exclude_unset=True)
        
        try:
            result = supabase.table("distractions").insert(distraction_data).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear el registro de distracción"
                )
            
            return DistractionResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el registro de distracción: {str(e)}"
            )
    
    @staticmethod
    def get_distraction_by_id(distraction_id: int) -> DistractionResponse:
        """Obtener un registro de distracción por ID"""
        supabase = get_supabase()
        
        try:
            result = supabase.table("distractions").select("*").eq("id", distraction_id).execute()
            
            if not result.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Distracción con ID {distraction_id} no encontrada"
                )
            
            return DistractionResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la distracción: {str(e)}"
            )
    
    @staticmethod
    def get_distractions_by_pomodoro_id(pomodoro_id: int) -> List[DistractionResponse]:
        """Obtener todas las distracciones de un pomodoro"""
        supabase = get_supabase()
        
        # Verificar que el pomodoro existe
        PomodoroService.get_pomodoro_by_id(pomodoro_id)
        
        try:
            result = supabase.table("distractions").select("*").eq("pomodoro_id", pomodoro_id).order("created_at", desc=True).execute()
            
            return [DistractionResponse(**d) for d in result.data] if result.data else []
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener las distracciones: {str(e)}"
            )
    
    @staticmethod
    def get_all_distractions(user_id: str = None) -> List[DistractionResponse]:
        """Obtener todas las distracciones, opcionalmente filtradas por user_id"""
        supabase = get_supabase()
        
        try:
            query = supabase.table("distractions").select("*")
            
            if user_id:
                query = query.eq("user_id", user_id)
            
            result = query.order("created_at", desc=True).execute()
            
            return [DistractionResponse(**d) for d in result.data] if result.data else []
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener las distracciones: {str(e)}"
            )
