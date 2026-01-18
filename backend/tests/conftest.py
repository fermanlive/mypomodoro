"""
Configuración global de pytest y fixtures compartidas
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from fastapi.testclient import TestClient
from typing import Generator
from datetime import datetime
from app.main import app
from app.models.schemas import TaskCategory, PomodoroMode


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Cliente de prueba para FastAPI"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def mock_supabase(monkeypatch):
    """Mock del cliente Supabase - se aplica automáticamente a todos los tests"""
    mock_client = MagicMock()
    
    def mock_get_supabase():
        return mock_client
    
    # Usar monkeypatch para asegurar que el mock se aplique antes de importar
    monkeypatch.setattr('app.database.supabase_client.get_supabase', mock_get_supabase)
    monkeypatch.setattr('app.services.task_service.get_supabase', mock_get_supabase)
    monkeypatch.setattr('app.services.subtask_service.get_supabase', mock_get_supabase)
    monkeypatch.setattr('app.services.pomodoro_service.get_supabase', mock_get_supabase)
    monkeypatch.setattr('app.services.distraction_service.get_supabase', mock_get_supabase)
    
    yield mock_client


@pytest.fixture
def sample_task_data():
    """Datos de ejemplo para una tarea"""
    return {
        "id": 1,
        "title": "Tarea de prueba",
        "completed": False,
        "category": "personal",
        "custom_category": None,
        "time_spent": 0,
        "user_id": None,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    }


@pytest.fixture
def sample_subtask_data():
    """Datos de ejemplo para una subtarea"""
    return {
        "id": 1,
        "task_id": 1,
        "title": "Subtarea de prueba",
        "completed": False,
        "time_spent": 0,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    }


@pytest.fixture
def sample_pomodoro_data():
    """Datos de ejemplo para un pomodoro"""
    return {
        "id": 1,
        "mode": "pomodoro",
        "objective": "Completar tarea de prueba",
        "task_id": 1,
        "subtask_ids": [1, 2],
        "duration": 1500,
        "completed": False,
        "started_at": None,
        "completed_at": None,
        "user_id": None,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    }


@pytest.fixture
def sample_distraction_data():
    """Datos de ejemplo para una distracción"""
    return {
        "id": 1,
        "pomodoro_id": 1,
        "had_distractions": True,
        "used_phone": False,
        "user_id": None,
        "created_at": "2024-01-01T10:00:00Z"
    }


@pytest.fixture
def mock_supabase_response():
    """Helper para crear respuestas mock de Supabase"""
    def _create_response(data=None, count=None):
        response = MagicMock()
        response.data = data or []
        response.count = count
        return response
    return _create_response


@pytest.fixture
def mock_table_query(mock_supabase):
    """Mock para las operaciones de tabla de Supabase"""
    def _setup_table_mock(table_name):
        table_mock = MagicMock()
        mock_supabase.table.return_value = table_mock
        
        # Configurar chain de métodos (select, eq, etc.)
        chain_mock = MagicMock()
        table_mock.select.return_value = chain_mock
        table_mock.insert.return_value = chain_mock
        table_mock.update.return_value = chain_mock
        table_mock.delete.return_value = chain_mock
        chain_mock.eq.return_value = chain_mock
        chain_mock.ilike.return_value = chain_mock
        chain_mock.order.return_value = chain_mock
        
        return table_mock, chain_mock
    
    return _setup_table_mock
