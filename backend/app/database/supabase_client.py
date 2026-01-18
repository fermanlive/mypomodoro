"""
Cliente de Supabase para la aplicación
"""

from supabase import create_client, Client
from app.config import settings


class SupabaseClient:
    """Cliente singleton para Supabase"""
    
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Obtener instancia del cliente Supabase"""
        if cls._instance is None:
            cls._instance = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
        return cls._instance
    
    @classmethod
    def reset_client(cls):
        """Resetear la instancia (útil para testing)"""
        cls._instance = None


# Función helper para obtener el cliente
def get_supabase() -> Client:
    """Helper function para obtener el cliente Supabase"""
    return SupabaseClient.get_client()
