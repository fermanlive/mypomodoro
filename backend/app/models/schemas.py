"""
Esquemas Pydantic para validación de datos
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums
class TaskCategory(str, Enum):
    """Categorías de tareas"""
    PERSONAL = "personal"
    LABORAL = "laboral"
    OTRO = "otro"


class PomodoroMode(str, Enum):
    """Modos del temporizador Pomodoro"""
    POMODORO = "pomodoro"
    SHORT_BREAK = "shortBreak"
    LONG_BREAK = "longBreak"


# Schemas de Subtareas
class SubtaskBase(BaseModel):
    """Schema base para subtareas"""
    title: str = Field(..., min_length=1, max_length=500)
    completed: bool = False
    time_spent: int = 0  # En segundos


class SubtaskCreate(SubtaskBase):
    """Schema para crear una subtarea"""
    task_id: int


class SubtaskUpdate(BaseModel):
    """Schema para actualizar una subtarea"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    completed: Optional[bool] = None
    time_spent: Optional[int] = Field(None, ge=0)


class SubtaskResponse(SubtaskBase):
    """Schema de respuesta para subtareas"""
    id: int
    task_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Schemas de Tareas
class TaskBase(BaseModel):
    """Schema base para tareas"""
    title: str = Field(..., min_length=1, max_length=500)
    completed: bool = False
    category: TaskCategory = TaskCategory.PERSONAL
    custom_category: Optional[str] = Field(None, max_length=100)
    time_spent: int = 0  # En segundos (suma de subtareas)
    user_id: Optional[str] = None  # Para multi-usuario en el futuro


class TaskCreate(TaskBase):
    """Schema para crear una tarea"""
    pass


class TaskUpdate(BaseModel):
    """Schema para actualizar una tarea"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    completed: Optional[bool] = None
    category: Optional[TaskCategory] = None
    custom_category: Optional[str] = Field(None, max_length=100)
    time_spent: Optional[int] = Field(None, ge=0)


class TaskResponse(TaskBase):
    """Schema de respuesta para tareas con subtareas"""
    id: int
    created_at: datetime
    updated_at: datetime
    subtasks: List[SubtaskResponse] = []
    
    class Config:
        from_attributes = True


# Schemas de Pomodoros
class PomodoroBase(BaseModel):
    """Schema base para pomodoros"""
    mode: PomodoroMode = PomodoroMode.POMODORO
    objective: Optional[str] = Field(None, max_length=1000)
    task_id: Optional[int] = None
    subtask_ids: Optional[List[int]] = []
    duration: int = 1500  # Por defecto 25 minutos en segundos
    user_id: Optional[str] = None


class PomodoroCreate(PomodoroBase):
    """Schema para crear un pomodoro"""
    pass


class PomodoroUpdate(BaseModel):
    """Schema para actualizar un pomodoro"""
    mode: Optional[PomodoroMode] = None
    objective: Optional[str] = Field(None, max_length=1000)
    task_id: Optional[int] = None
    subtask_ids: Optional[List[int]] = None


class PomodoroResponse(PomodoroBase):
    """Schema de respuesta para pomodoros"""
    id: int
    completed: bool = False
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PomodoroComplete(BaseModel):
    """Schema para completar un pomodoro"""
    pomodoro_id: int
    actual_duration: Optional[int] = None  # Duración real en segundos


# Schemas de Distracciones
class DistractionBase(BaseModel):
    """Schema base para distracciones"""
    pomodoro_id: int
    had_distractions: bool
    used_phone: bool
    user_id: Optional[str] = None


class DistractionCreate(DistractionBase):
    """Schema para crear un registro de distracción"""
    pass


class DistractionResponse(DistractionBase):
    """Schema de respuesta para distracciones"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Schemas de Estadísticas
class TaskStats(BaseModel):
    """Estadísticas de una tarea"""
    task_id: int
    task_title: str
    total_time_spent: int
    pomodoros_completed: int
    completion_percentage: float


class CategoryStats(BaseModel):
    """Estadísticas por categoría"""
    category: str
    total_time_spent: int
    pomodoros_completed: int
    tasks_count: int


class StatisticsResponse(BaseModel):
    """Respuesta de estadísticas generales"""
    total_pomodoros: int
    total_time_spent: int  # En segundos
    tasks_stats: List[TaskStats]
    category_stats: List[CategoryStats]
    distractions_count: int
    phone_usage_count: int
