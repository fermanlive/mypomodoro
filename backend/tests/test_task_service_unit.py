"""
Tests UNITARIOS para TaskService
Cada método se prueba de forma aislada, mockeando todas las dependencias
"""

import pytest
from unittest.mock import MagicMock, patch, call
from fastapi import HTTPException, status
from app.services.task_service import TaskService
from app.models.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskCategory


class TestTaskServiceUnit:
    """Tests unitarios aislados para TaskService"""
    
    @patch('app.services.task_service.get_supabase')
    @patch.object(TaskService, 'get_task_by_id')
    def test_create_task_unit(self, mock_get_task, mock_get_supabase, sample_task_data):
        """Test unitario: crear tarea - solo prueba la lógica de insert"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        insert_response = MagicMock()
        insert_response.data = [sample_task_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        # Mock para get_task_by_id (que será llamado después)
        mock_get_task.return_value = TaskResponse(**sample_task_data, subtasks=[])
        
        task_create = TaskCreate(title="Tarea de prueba", category=TaskCategory.PERSONAL)
        
        # Act
        result = TaskService.create_task(task_create)
        
        # Assert - Solo verificamos que se llama insert y get_task_by_id
        mock_supabase.table.assert_called_once_with("tasks")
        mock_supabase.table.return_value.insert.assert_called_once()
        mock_get_task.assert_called_once_with(sample_task_data["id"])
        assert isinstance(result, TaskResponse)
    
    @patch('app.services.task_service.get_supabase')
    def test_create_task_error_unit(self, mock_get_supabase):
        """Test unitario: error al crear tarea"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        insert_response = MagicMock()
        insert_response.data = None
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        task_create = TaskCreate(title="Tarea de prueba")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            TaskService.create_task(task_create)
        
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @patch('app.services.task_service.get_supabase')
    def test_get_task_by_id_unit(self, mock_get_supabase, sample_task_data):
        """Test unitario: obtener tarea por ID - solo prueba la consulta y construcción"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock para obtener tarea
        task_response = MagicMock()
        task_response.data = [sample_task_data]
        
        # Mock para subtareas
        subtasks_response = MagicMock()
        subtasks_response.data = []
        
        # Configurar side_effect para múltiples llamadas
        mock_execute = MagicMock(side_effect=[task_response, subtasks_response])
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute = mock_execute
        mock_table.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        mock_supabase.table.return_value = mock_table
        
        # Act
        result = TaskService.get_task_by_id(1)
        
        # Assert
        assert isinstance(result, TaskResponse)
        assert result.id == 1
        assert result.title == "Tarea de prueba"
        # Verificar que se llamó a las tablas correctas
        assert mock_supabase.table.call_count == 2  # tasks y subtasks
    
    @patch('app.services.task_service.get_supabase')
    def test_get_task_by_id_not_found_unit(self, mock_get_supabase):
        """Test unitario: tarea no encontrada"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        task_response = MagicMock()
        task_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = task_response
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            TaskService.get_task_by_id(999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    @patch('app.services.task_service.get_supabase')
    def test_get_all_tasks_unit(self, mock_get_supabase, sample_task_data):
        """Test unitario: obtener todas las tareas"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        tasks_response = MagicMock()
        tasks_response.data = [sample_task_data]
        mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value = tasks_response
        
        subtasks_response = MagicMock()
        subtasks_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        # Act
        result = TaskService.get_all_tasks()
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].id == 1
    
    @patch('app.services.task_service.get_supabase')
    def test_get_all_tasks_with_search_unit(self, mock_get_supabase, sample_task_data):
        """Test unitario: búsqueda de tareas"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        tasks_response = MagicMock()
        tasks_response.data = [sample_task_data]
        
        # Mock para la cadena de query
        mock_query = MagicMock()
        mock_query.ilike.return_value.order.return_value.execute.return_value = tasks_response
        mock_supabase.table.return_value.select.return_value = mock_query
        
        subtasks_response = MagicMock()
        subtasks_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        # Act
        result = TaskService.get_all_tasks(search="prueba")
        
        # Assert
        assert len(result) == 1
        mock_query.ilike.assert_called_once_with("title", "%prueba%")
    
    @patch.object(TaskService, 'get_task_by_id')
    @patch('app.services.task_service.get_supabase')
    def test_update_task_unit(self, mock_get_supabase, mock_get_task, sample_task_data):
        """Test unitario: actualizar tarea - mockea get_task_by_id"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock para get_task_by_id (verificar existencia)
        task_response = TaskResponse(**sample_task_data, subtasks=[])
        mock_get_task.return_value = task_response
        
        # Mock para update
        updated_data = sample_task_data.copy()
        updated_data["title"] = "Tarea actualizada"
        update_response = MagicMock()
        update_response.data = [updated_data]
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = update_response
        
        # Mock para get_task_by_id después del update
        updated_task = TaskResponse(**updated_data, subtasks=[])
        mock_get_task.return_value = updated_task
        
        task_update = TaskUpdate(title="Tarea actualizada")
        
        # Act
        result = TaskService.update_task(1, task_update)
        
        # Assert
        assert result.title == "Tarea actualizada"
        # Verificar que se llamó get_task_by_id dos veces (verificar existencia + retornar actualizado)
        assert mock_get_task.call_count == 2
    
    @patch.object(TaskService, 'get_task_by_id')
    @patch('app.services.task_service.get_supabase')
    def test_delete_task_unit(self, mock_get_supabase, mock_get_task, sample_task_data):
        """Test unitario: eliminar tarea - mockea get_task_by_id"""
        # Arrange
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock para get_task_by_id (verificar existencia)
        task_response = TaskResponse(**sample_task_data, subtasks=[])
        mock_get_task.return_value = task_response
        
        # Mock para delete
        delete_response = MagicMock()
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = delete_response
        
        # Act
        result = TaskService.delete_task(1)
        
        # Assert
        assert result is True
        mock_get_task.assert_called_once_with(1)
        mock_supabase.table.assert_called_with("tasks")
