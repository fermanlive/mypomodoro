"""
Tests unitarios para DistractionService
"""

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from app.services.distraction_service import DistractionService
from app.models.schemas import DistractionCreate


class TestDistractionService:
    """Tests para DistractionService"""
    
    def test_create_distraction_success(self, mock_supabase, sample_distraction_data, sample_pomodoro_data):
        """Test crear distracción exitosamente"""
        # Mock para verificar que el pomodoro existe
        pomodoro_response = MagicMock()
        pomodoro_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = pomodoro_response
        
        # Mock para insert
        insert_response = MagicMock()
        insert_response.data = [sample_distraction_data]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = insert_response
        
        distraction_create = DistractionCreate(
            pomodoro_id=1,
            had_distractions=True,
            used_phone=False
        )
        
        result = DistractionService.create_distraction(distraction_create)
        
        assert result.pomodoro_id == 1
        assert result.had_distractions is True
        assert result.used_phone is False
    
    def test_get_distraction_by_id_success(self, mock_supabase, sample_distraction_data):
        """Test obtener distracción por ID"""
        distraction_response = MagicMock()
        distraction_response.data = [sample_distraction_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = distraction_response
        
        result = DistractionService.get_distraction_by_id(1)
        
        assert result.id == 1
        assert result.had_distractions is True
    
    def test_get_distraction_by_id_not_found(self, mock_supabase):
        """Test obtener distracción inexistente"""
        distraction_response = MagicMock()
        distraction_response.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = distraction_response
        
        with pytest.raises(HTTPException) as exc_info:
            DistractionService.get_distraction_by_id(999)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_distractions_by_pomodoro_id(self, mock_supabase, sample_distraction_data, sample_pomodoro_data):
        """Test obtener distracciones de un pomodoro"""
        # Mock para verificar pomodoro existe
        pomodoro_response = MagicMock()
        pomodoro_response.data = [sample_pomodoro_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = pomodoro_response
        
        # Mock para obtener distracciones
        distractions_response = MagicMock()
        distractions_response.data = [sample_distraction_data]
        mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = distractions_response
        
        result = DistractionService.get_distractions_by_pomodoro_id(1)
        
        assert isinstance(result, list)
        assert len(result) == 1
