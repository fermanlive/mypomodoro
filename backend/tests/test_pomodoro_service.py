"""
Tests unitarios para PomodoroService
"""

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from app.services.pomodoro_service import PomodoroService
from app.models.schemas import PomodoroCreate, PomodoroUpdate, PomodoroComplete, PomodoroMode


class TestPomodoroService:
    """Tests para PomodoroService"""
    
    def test_create_pomodoro_success(self, mock_supabase, sample_pomodoro_data):
        """Test crear pomodoro exitosamente"""
        insert_response = MagicMock()
        insert_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        pomodoro_create = PomodoroCreate(
            mode=PomodoroMode.POMODORO,
            objective="Completar tarea"
        )
        
        result = PomodoroService.create_pomodoro(pomodoro_create)
        
        assert result.mode == PomodoroMode.POMODORO
        assert result.objective == "Completar tarea"
        assert result.duration == 1500  # Default para pomodoro
    
    def test_create_pomodoro_with_custom_duration(self, mock_supabase, sample_pomodoro_data):
        """Test crear pomodoro con duración personalizada"""
        sample_pomodoro_data["duration"] = 1800
        insert_response = MagicMock()
        insert_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        pomodoro_create = PomodoroCreate(
            mode=PomodoroMode.POMODORO,
            duration=1800
        )
        
        result = PomodoroService.create_pomodoro(pomodoro_create)
        assert result.duration == 1800
    
    def test_get_pomodoro_by_id_success(self, mock_supabase, sample_pomodoro_data):
        """Test obtener pomodoro por ID"""
        pomodoro_response = MagicMock()
        pomodoro_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = pomodoro_response
        
        result = PomodoroService.get_pomodoro_by_id(1)
        
        assert result.id == 1
        assert result.mode == PomodoroMode.POMODORO
    
    def test_get_pomodoro_by_id_not_found(self, mock_supabase):
        """Test obtener pomodoro inexistente"""
        pomodoro_response = MagicMock()
        pomodoro_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = pomodoro_response
        
        with pytest.raises(HTTPException) as exc_info:
            PomodoroService.get_pomodoro_by_id(999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_all_pomodoros(self, mock_supabase, sample_pomodoro_data):
        """Test obtener todos los pomodoros"""
        pomodoros_response = MagicMock()
        pomodoros_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value = pomodoros_response
        
        result = PomodoroService.get_all_pomodoros()
        
        assert isinstance(result, list)
        assert len(result) == 1
    
    def test_get_all_pomodoros_with_filters(self, mock_supabase, sample_pomodoro_data):
        """Test obtener pomodoros con filtros"""
        pomodoros_response = MagicMock()
        pomodoros_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = pomodoros_response
        
        result = PomodoroService.get_all_pomodoros(completed=True)
        
        assert isinstance(result, list)
    
    def test_update_pomodoro_success(self, mock_supabase, sample_pomodoro_data):
        """Test actualizar pomodoro"""
        # Mock para get_pomodoro_by_id
        pomodoro_response = MagicMock()
        pomodoro_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = pomodoro_response
        
        # Mock para update
        updated_data = sample_pomodoro_data.copy()
        updated_data["objective"] = "Objetivo actualizado"
        update_response = MagicMock()
        update_response.data = [updated_data]
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = update_response
        
        pomodoro_update = PomodoroUpdate(objective="Objetivo actualizado")
        result = PomodoroService.update_pomodoro(1, pomodoro_update)
        
        assert result.objective == "Objetivo actualizado"
    
    def test_complete_pomodoro_success(self, mock_supabase, sample_pomodoro_data, sample_subtask_data):
        """Test completar pomodoro y actualizar tiempos"""
        # Mock para get_pomodoro_by_id
        pomodoro_response = MagicMock()
        pomodoro_response.data = [sample_pomodoro_data]
        
        # Mock para obtener subtareas
        subtask_response = MagicMock()
        subtask_response.data = [sample_subtask_data]
        
        # Configurar mocks
        calls = [pomodoro_response]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = calls
        
        # Mock para actualizar subtareas (time_spent)
        update_subtask_response = MagicMock()
        updated_subtask = sample_subtask_data.copy()
        updated_subtask["time_spent"] = 1500
        update_subtask_response.data = [updated_subtask]
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = update_subtask_response
        
        # Mock para actualizar pomodoro
        updated_pomodoro = sample_pomodoro_data.copy()
        updated_pomodoro["completed"] = True
        update_pomodoro_response = MagicMock()
        update_pomodoro_response.data = [updated_pomodoro]
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = update_pomodoro_response
        
        pomodoro_complete = PomodoroComplete(pomodoro_id=1)
        result = PomodoroService.complete_pomodoro(pomodoro_complete)
        
        assert result.completed is True
