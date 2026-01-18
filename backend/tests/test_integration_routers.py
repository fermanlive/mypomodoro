"""
Tests de INTEGRACIÓN para los routers (endpoints API)
Estos NO son tests unitarios - prueban la integración completa del endpoint
"""

import pytest
from unittest.mock import patch, MagicMock
from app.models.schemas import TaskCategory, PomodoroMode


class TestTasksRouterIntegration:
    """Tests de integración para el router de tareas"""
    
    def test_create_task_endpoint_integration(self, client, mock_supabase, sample_task_data):
        """Test de integración: POST /api/v1/tasks/"""
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
    
    def test_get_tasks_endpoint_integration(self, client, mock_supabase, sample_task_data):
        """Test de integración: GET /api/v1/tasks/"""
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


class TestHealthEndpointsIntegration:
    """Tests de integración para endpoints de salud"""
    
    def test_root_endpoint_integration(self, client):
        """Test de integración: GET /"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "MyPomodoro API"
    
    def test_health_endpoint_integration(self, client):
        """Test de integración: GET /health"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
