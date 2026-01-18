"""
Tests unitarios para los routers (endpoints API)
"""

import pytest
from unittest.mock import patch, MagicMock
from app.models.schemas import TaskCategory, PomodoroMode


class TestTasksRouter:
    """Tests para el router de tareas"""
    
    def test_create_task_endpoint(self, client, mock_supabase, sample_task_data):
        """Test POST /api/v1/tasks/"""
        # Setup mocks
        insert_response = MagicMock()
        insert_response.data = [sample_task_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        get_response = MagicMock()
        get_response.data = [sample_task_data]
        
        subtasks_response = MagicMock()
        subtasks_response.data = []
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [get_response, subtasks_response]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Tarea de prueba",
                "category": "personal"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Tarea de prueba"
    
    def test_get_tasks_endpoint(self, client, mock_supabase, sample_task_data):
        """Test GET /api/v1/tasks/"""
        tasks_response = MagicMock()
        tasks_response.data = [sample_task_data]
        mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value = tasks_response
        
        subtasks_response = MagicMock()
        subtasks_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        response = client.get("/api/v1/tasks/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
    
    def test_get_task_by_id_endpoint(self, client, mock_supabase, sample_task_data):
        """Test GET /api/v1/tasks/{task_id}"""
        task_response = MagicMock()
        task_response.data = [sample_task_data]
        
        subtasks_response = MagicMock()
        subtasks_response.data = []
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [task_response, subtasks_response]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        response = client.get("/api/v1/tasks/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
    
    def test_update_task_endpoint(self, client, mock_supabase, sample_task_data):
        """Test PUT /api/v1/tasks/{task_id}"""
        # Mock para get_task_by_id
        task_response = MagicMock()
        task_response.data = [sample_task_data]
        
        subtasks_response = MagicMock()
        subtasks_response.data = []
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [task_response, subtasks_response]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        # Mock para update
        updated_data = sample_task_data.copy()
        updated_data["title"] = "Tarea actualizada"
        update_response = MagicMock()
        update_response.data = [updated_data]
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = update_response
        
        # Mock para get después del update
        updated_task_response = MagicMock()
        updated_task_response.data = [updated_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
            updated_task_response,
            subtasks_response
        ]
        
        response = client.put(
            "/api/v1/tasks/1",
            json={"title": "Tarea actualizada"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Tarea actualizada"
    
    def test_delete_task_endpoint(self, client, mock_supabase, sample_task_data):
        """Test DELETE /api/v1/tasks/{task_id}"""
        # Mock para get_task_by_id
        task_response = MagicMock()
        task_response.data = [sample_task_data]
        
        subtasks_response = MagicMock()
        subtasks_response.data = []
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [task_response, subtasks_response]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = subtasks_response
        
        # Mock para delete
        delete_response = MagicMock()
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = delete_response
        
        response = client.delete("/api/v1/tasks/1")
        
        assert response.status_code == 204


class TestPomodorosRouter:
    """Tests para el router de pomodoros"""
    
    def test_create_pomodoro_endpoint(self, client, mock_supabase, sample_pomodoro_data):
        """Test POST /api/v1/pomodoros/"""
        insert_response = MagicMock()
        insert_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        response = client.post(
            "/api/v1/pomodoros/",
            json={
                "mode": "pomodoro",
                "objective": "Completar tarea"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "pomodoro"
    
    def test_get_pomodoros_endpoint(self, client, mock_supabase, sample_pomodoro_data):
        """Test GET /api/v1/pomodoros/"""
        pomodoros_response = MagicMock()
        pomodoros_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value = pomodoros_response
        
        response = client.get("/api/v1/pomodoros/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestHealthEndpoint:
    """Tests para endpoints de salud"""
    
    def test_root_endpoint(self, client):
        """Test GET /"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "MyPomodoro API"
    
    def test_health_endpoint(self, client):
        """Test GET /health"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
