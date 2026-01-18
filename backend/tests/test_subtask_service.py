"""
Tests unitarios para SubtaskService
"""

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from app.services.subtask_service import SubtaskService
from app.models.schemas import SubtaskCreate, SubtaskUpdate
from app.services.task_service import TaskService


class TestSubtaskService:
    """Tests para SubtaskService"""
    
    def test_create_subtask_success(self, mock_supabase, sample_subtask_data, sample_task_data):
        """Test crear subtarea exitosamente"""
        # Mock para verificar que la tarea existe (TaskService.get_task_by_id)
        task_response = MagicMock()
        task_response.data = [sample_task_data]
        
        subtasks_empty = MagicMock()
        subtasks_empty.data = []
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [task_response, subtasks_empty]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_empty
        
        # Mock para insert
        insert_response = MagicMock()
        insert_response.data = [sample_subtask_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        subtask_create = SubtaskCreate(
            title="Subtarea de prueba",
            task_id=1
        )
        
        result = SubtaskService.create_subtask(subtask_create)
        
        assert result.id == 1
        assert result.title == "Subtarea de prueba"
        assert result.task_id == 1
    
    def test_get_subtask_by_id_success(self, mock_supabase, sample_subtask_data):
        """Test obtener subtarea por ID"""
        subtask_response = MagicMock()
        subtask_response.data = [sample_subtask_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = subtask_response
        
        result = SubtaskService.get_subtask_by_id(1)
        
        assert result.id == 1
        assert result.title == "Subtarea de prueba"
    
    def test_get_subtask_by_id_not_found(self, mock_supabase):
        """Test obtener subtarea inexistente"""
        subtask_response = MagicMock()
        subtask_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = subtask_response
        
        with pytest.raises(HTTPException) as exc_info:
            SubtaskService.get_subtask_by_id(999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_subtasks_by_task_id(self, mock_supabase, sample_subtask_data, sample_task_data):
        """Test obtener subtareas de una tarea"""
        # Mock para verificar tarea existe
        task_response = MagicMock()
        task_response.data = [sample_task_data]
        
        subtasks_empty = MagicMock()
        subtasks_empty.data = []
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [task_response]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = MagicMock(data=[sample_subtask_data])
        
        result = SubtaskService.get_subtasks_by_task_id(1)
        
        assert isinstance(result, list)
        assert len(result) == 1
    
    def test_update_subtask_success(self, mock_supabase, sample_subtask_data):
        """Test actualizar subtarea"""
        # Mock para get_subtask_by_id
        subtask_response = MagicMock()
        subtask_response.data = [sample_subtask_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = subtask_response
        
        # Mock para update
        updated_data = sample_subtask_data.copy()
        updated_data["title"] = "Subtarea actualizada"
        update_response = MagicMock()
        update_response.data = [updated_data]
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = update_response
        
        subtask_update = SubtaskUpdate(title="Subtarea actualizada")
        result = SubtaskService.update_subtask(1, subtask_update)
        
        assert result.title == "Subtarea actualizada"
    
    def test_delete_subtask_success(self, mock_supabase, sample_subtask_data):
        """Test eliminar subtarea"""
        # Mock para get_subtask_by_id
        subtask_response = MagicMock()
        subtask_response.data = [sample_subtask_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = subtask_response
        
        # Mock para delete
        delete_response = MagicMock()
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = delete_response
        
        result = SubtaskService.delete_subtask(1)
        
        assert result is True
