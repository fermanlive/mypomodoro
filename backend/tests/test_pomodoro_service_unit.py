"""
Tests UNITARIOS para PomodoroService
Cada método se prueba de forma aislada, mockeando todas las dependencias
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from app.services.pomodoro_service import PomodoroService
from app.models.schemas import PomodoroCreate, PomodoroUpdate, PomodoroComplete, PomodoroMode


class TestPomodoroServiceUnit:
    """Tests unitarios aislados para PomodoroService"""
    
    @patch('app.services.pomodoro_service.TaskService')
    @patch('app.services.pomodoro_service.get_supabase')
    def test_create_pomodoro_unit(self, mock_get_supabase, mock_task_service):
        """Test unitario: crear pomodoro - mockea TaskService si hay task_id"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        sample_pomodoro_data = {
            "id": 1,
            "mode": "pomodoro",
            "objective": "Completar tarea",
            "task_id": 1,
            "subtask_ids": [],
            "duration": 1500,
            "completed": False,
            "started_at": None,
            "completed_at": None,
            "user_id": None,
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z"
        }
        
        mock_task_service.get_task_by_id.return_value = MagicMock(id=1)
        insert_response = MagicMock()
        insert_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        pomodoro_create = PomodoroCreate(mode=PomodoroMode.POMODORO, objective="Completar tarea", task_id=1)
        
        # Act
        result = PomodoroService.create_pomodoro(pomodoro_create)
        
        # Assert
        assert result.mode == PomodoroMode.POMODORO
        mock_task_service.get_task_by_id.assert_called_once_with(1)
    
    @patch('app.services.pomodoro_service.get_supabase')
    def test_create_pomodoro_without_task_id_unit(self, mock_get_supabase):
        """Test unitario: crear pomodoro sin task_id"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        sample_pomodoro_data = {
            "id": 1,
            "mode": "shortBreak",
            "objective": None,
            "task_id": None,
            "subtask_ids": [],
            "duration": 300,
            "completed": False,
            "started_at": None,
            "completed_at": None,
            "user_id": None,
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z"
        }
        
        insert_response = MagicMock()
        insert_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        pomodoro_create = PomodoroCreate(mode=PomodoroMode.SHORT_BREAK)
        
        # Act
        result = PomodoroService.create_pomodoro(pomodoro_create)
        
        # Assert
        assert result.mode == PomodoroMode.SHORT_BREAK
        assert result.duration == 300  # 5 minutos
    
    @patch('app.services.pomodoro_service.get_supabase')
    def test_get_pomodoro_by_id_unit(self, mock_get_supabase):
        """Test unitario: obtener pomodoro por ID"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        sample_pomodoro_data = {
            "id": 1,
            "mode": "pomodoro",
            "objective": "Test",
            "task_id": None,
            "subtask_ids": [],
            "duration": 1500,
            "completed": False,
            "started_at": None,
            "completed_at": None,
            "user_id": None,
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z"
        }
        
        pomodoro_response = MagicMock()
        pomodoro_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = pomodoro_response
        
        # Act
        result = PomodoroService.get_pomodoro_by_id(1)
        
        # Assert
        assert result.id == 1
        assert result.mode == PomodoroMode.POMODORO
    
    @patch('app.services.pomodoro_service.get_supabase')
    def test_get_pomodoro_by_id_not_found_unit(self, mock_get_supabase):
        """Test unitario: pomodoro no encontrado"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        pomodoro_response = MagicMock()
        pomodoro_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = pomodoro_response
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            PomodoroService.get_pomodoro_by_id(999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    @patch.object(PomodoroService, 'get_pomodoro_by_id')
    @patch('app.services.pomodoro_service.SubtaskService')
    @patch('app.services.pomodoro_service.get_supabase')
    def test_complete_pomodoro_unit(self, mock_get_supabase, mock_subtask_service, mock_get_pomodoro):
        """Test unitario: completar pomodoro - mockea todas las dependencias"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock para get_pomodoro_by_id
        from app.models.schemas import PomodoroResponse
        from datetime import datetime
        pomodoro = PomodoroResponse(
            id=1,
            mode=PomodoroMode.POMODORO,
            subtask_ids=[1, 2],
            duration=1500,
            completed=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        mock_get_pomodoro.return_value = pomodoro
        
        # Mock para SubtaskService
        from app.models.schemas import SubtaskResponse
        mock_subtask = SubtaskResponse(
            id=1,
            task_id=1,
            title="Subtarea",
            completed=False,
            time_spent=0,
            created_at="2024-01-01T10:00:00Z",
            updated_at="2024-01-01T10:00:00Z"
        )
        mock_subtask_service.get_subtask_by_id.return_value = mock_subtask
        mock_subtask_service.update_subtask.return_value = mock_subtask
        
        # Mock para update del pomodoro
        updated_pomodoro_data = {
            "id": 1,
            "mode": "pomodoro",
            "completed": True,
            "duration": 1500,
            "completed_at": "2024-01-01T11:00:00Z",
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T11:00:00Z"
        }
        update_response = MagicMock()
        update_response.data = [updated_pomodoro_data]
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = update_response
        
        pomodoro_complete = PomodoroComplete(pomodoro_id=1)
        
        # Act
        result = PomodoroService.complete_pomodoro(pomodoro_complete)
        
        # Assert
        assert result.completed is True
        # Verificar que se llamó a actualizar cada subtarea
        assert mock_subtask_service.get_subtask_by_id.call_count == 2
        assert mock_subtask_service.update_subtask.call_count == 2
