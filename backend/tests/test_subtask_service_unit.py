"""
Tests UNITARIOS para SubtaskService
Cada método se prueba de forma aislada, mockeando todas las dependencias externas
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from app.services.subtask_service import SubtaskService
from app.models.schemas import SubtaskCreate, SubtaskUpdate, SubtaskResponse


class TestSubtaskServiceUnit:
    """Tests unitarios aislados para SubtaskService"""
    
    @patch('app.services.subtask_service.TaskService')
    @patch('app.services.subtask_service.get_supabase')
    def test_create_subtask_unit(self, mock_get_supabase, mock_task_service, sample_subtask_data):
        """Test unitario: crear subtarea - mockea TaskService"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock para TaskService.get_task_by_id
        mock_task_service.get_task_by_id.return_value = MagicMock(id=1)
        
        # Mock para insert
        insert_response = MagicMock()
        insert_response.data = [sample_subtask_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        subtask_create = SubtaskCreate(title="Subtarea de prueba", task_id=1)
        
        # Act
        result = SubtaskService.create_subtask(subtask_create)
        
        # Assert
        assert result.id == 1
        assert result.title == "Subtarea de prueba"
        mock_task_service.get_task_by_id.assert_called_once_with(1)
    
    @patch('app.services.subtask_service.get_supabase')
    def test_get_subtask_by_id_unit(self, mock_get_supabase, sample_subtask_data):
        """Test unitario: obtener subtarea por ID"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        subtask_response = MagicMock()
        subtask_response.data = [sample_subtask_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = subtask_response
        
        # Act
        result = SubtaskService.get_subtask_by_id(1)
        
        # Assert
        assert result.id == 1
        assert result.title == "Subtarea de prueba"
    
    @patch('app.services.subtask_service.get_supabase')
    def test_get_subtask_by_id_not_found_unit(self, mock_get_supabase):
        """Test unitario: subtarea no encontrada"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        subtask_response = MagicMock()
        subtask_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = subtask_response
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            SubtaskService.get_subtask_by_id(999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    @patch('app.services.subtask_service.TaskService')
    @patch('app.services.subtask_service.get_supabase')
    def test_get_subtasks_by_task_id_unit(self, mock_get_supabase, mock_task_service):
        """Test unitario: obtener subtareas de una tarea - mockea TaskService"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock para verificar tarea existe
        mock_task_service.get_task_by_id.return_value = MagicMock(id=1)
        
        # Mock para obtener subtareas
        sample_subtask = {
            "id": 1,
            "task_id": 1,
            "title": "Subtarea",
            "completed": False,
            "time_spent": 0,
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z"
        }
        subtasks_response = MagicMock()
        subtasks_response.data = [sample_subtask]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        # Act
        result = SubtaskService.get_subtasks_by_task_id(1)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        mock_task_service.get_task_by_id.assert_called_once_with(1)
    
    @patch('app.services.subtask_service.get_supabase')
    def test_update_subtask_unit(self, mock_get_supabase, sample_subtask_data):
        """Test unitario: actualizar subtarea"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock para get_subtask_by_id (que será llamado primero)
        with patch.object(SubtaskService, 'get_subtask_by_id') as mock_get:
            mock_get.return_value = SubtaskResponse(**sample_subtask_data)
            
            # Mock para update
            updated_data = sample_subtask_data.copy()
            updated_data["title"] = "Subtarea actualizada"
            update_response = MagicMock()
            update_response.data = [updated_data]
            mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = update_response
            
            subtask_update = SubtaskUpdate(title="Subtarea actualizada")
            
            # Act
            result = SubtaskService.update_subtask(1, subtask_update)
            
            # Assert
            assert result.title == "Subtarea actualizada"
    
    @patch('app.services.subtask_service.get_supabase')
    def test_delete_subtask_unit(self, mock_get_supabase, sample_subtask_data):
        """Test unitario: eliminar subtarea"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock para get_subtask_by_id
        with patch.object(SubtaskService, 'get_subtask_by_id') as mock_get:
            mock_get.return_value = SubtaskResponse(**sample_subtask_data)
            
            # Mock para delete
            delete_response = MagicMock()
            mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = delete_response
            
            # Act
            result = SubtaskService.delete_subtask(1)
            
            # Assert
            assert result is True
