"""
Tests unitarios para TaskService
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from app.services.task_service import TaskService
from app.models.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskCategory


class TestTaskService:
    """Tests para TaskService"""
    
    def test_create_task_success(self, mock_supabase, sample_task_data, sample_subtask_data):
        """Test crear tarea exitosamente"""
        # Setup mocks
        insert_response = MagicMock()
        insert_response.data = [sample_task_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        get_response = MagicMock()
        get_response.data = [sample_task_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = get_response
        
        # Mock para subtareas (vacías)
        subtasks_response = MagicMock()
        subtasks_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        # Crear tarea
        task_create = TaskCreate(
            title="Tarea de prueba",
            category=TaskCategory.PERSONAL
        )
        
        result = TaskService.create_task(task_create)
        
        assert isinstance(result, TaskResponse)
        assert result.title == "Tarea de prueba"
        assert result.category == TaskCategory.PERSONAL
    
    def test_create_task_error(self, mock_supabase):
        """Test crear tarea con error"""
        # Mock que falla
        insert_response = MagicMock()
        insert_response.data = None
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        task_create = TaskCreate(title="Tarea de prueba")
        
        with pytest.raises(HTTPException) as exc_info:
            TaskService.create_task(task_create)
        
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def test_get_task_by_id_success(self, mock_supabase, sample_task_data):
        """Test obtener tarea por ID exitosamente"""
        # Mock para obtener tarea
        task_response = MagicMock()
        task_response.data = [sample_task_data]
        
        # Mock para subtareas
        subtasks_response = MagicMock()
        subtasks_response.data = []
        
        # Configurar mocks para diferentes llamadas
        calls = [task_response, subtasks_response]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = calls
        
        # Configurar mock para order (subtareas)
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        result = TaskService.get_task_by_id(1)
        
        assert isinstance(result, TaskResponse)
        assert result.id == 1
        assert result.title == "Tarea de prueba"
    
    def test_get_task_by_id_not_found(self, mock_supabase):
        """Test obtener tarea inexistente"""
        task_response = MagicMock()
        task_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = task_response
        
        with pytest.raises(HTTPException) as exc_info:
            TaskService.get_task_by_id(999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_all_tasks(self, mock_supabase, sample_task_data):
        """Test obtener todas las tareas"""
        # Mock para lista de tareas
        tasks_response = MagicMock()
        tasks_response.data = [sample_task_data]
        mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value = tasks_response
        
        # Mock para subtareas de cada tarea
        subtasks_response = MagicMock()
        subtasks_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        result = TaskService.get_all_tasks()
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].id == 1
    
    def test_get_all_tasks_with_search(self, mock_supabase, sample_task_data):
        """Test obtener tareas con búsqueda"""
        tasks_response = MagicMock()
        tasks_response.data = [sample_task_data]
        mock_supabase.table.return_value.select.return_value.ilike.return_value.order.return_value.execute.return_value = tasks_response
        
        subtasks_response = MagicMock()
        subtasks_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        result = TaskService.get_all_tasks(search="prueba")
        
        assert len(result) == 1
    
    def test_update_task_success(self, mock_supabase, sample_task_data):
        """Test actualizar tarea exitosamente"""
        # Mock para get_task_by_id (primera llamada)
        task_response = MagicMock()
        task_response.data = [sample_task_data]
        
        subtasks_response = MagicMock()
        subtasks_response.data = []
        
        # Configurar mocks
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [task_response, subtasks_response]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        # Mock para update
        updated_data = sample_task_data.copy()
        updated_data["title"] = "Tarea actualizada"
        update_response = MagicMock()
        update_response.data = [updated_data]
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = update_response
        
        # Mock para get_task_by_id después del update
        updated_task_response = MagicMock()
        updated_task_response.data = [updated_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
            updated_task_response,
            subtasks_response
        ]
        
        task_update = TaskUpdate(title="Tarea actualizada")
        result = TaskService.update_task(1, task_update)
        
        assert result.title == "Tarea actualizada"
    
    def test_delete_task_success(self, mock_supabase, sample_task_data):
        """Test eliminar tarea exitosamente"""
        # Mock para get_task_by_id (verificar existencia)
        task_response = MagicMock()
        task_response.data = [sample_task_data]
        
        subtasks_response = MagicMock()
        subtasks_response.data = []
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [task_response, subtasks_response]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        # Mock para delete
        delete_response = MagicMock()
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = delete_response
        
        result = TaskService.delete_task(1)
        
        assert result is True
