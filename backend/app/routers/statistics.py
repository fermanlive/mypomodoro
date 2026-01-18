"""
Router para endpoints de estadísticas
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.models.schemas import StatisticsResponse, TaskStats, CategoryStats
from app.database.supabase_client import get_supabase
from app.services.pomodoro_service import PomodoroService
from app.services.distraction_service import DistractionService
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/", response_model=StatisticsResponse)
async def get_statistics(user_id: Optional[str] = Query(None)):
    """Obtener estadísticas generales del usuario"""
    supabase = get_supabase()
    
    # Obtener todas las tareas
    tasks = TaskService.get_all_tasks(user_id=user_id)
    
    # Calcular estadísticas de tareas
    tasks_stats = []
    for task in tasks:
        # Contar pomodoros completados para esta tarea
        pomodoros_result = supabase.table("pomodoros").select("id").eq("task_id", task.id).eq("completed", True).execute()
        pomodoros_count = len(pomodoros_result.data) if pomodoros_result.data else 0
        
        # Calcular porcentaje de completitud
        total_subtasks = len(task.subtasks)
        completed_subtasks = len([st for st in task.subtasks if st.completed])
        completion_percentage = (completed_subtasks / total_subtasks * 100) if total_subtasks > 0 else 0
        
        tasks_stats.append(TaskStats(
            task_id=task.id,
            task_title=task.title,
            total_time_spent=task.time_spent,
            pomodoros_completed=pomodoros_count,
            completion_percentage=round(completion_percentage, 2)
        ))
    
    # Calcular estadísticas por categoría
    category_stats = {}
    for task in tasks:
        category = task.custom_category if task.category == "otro" and task.custom_category else task.category
        
        if category not in category_stats:
            category_stats[category] = {
                "total_time_spent": 0,
                "pomodoros_completed": 0,
                "tasks_count": 0
            }
        
        category_stats[category]["total_time_spent"] += task.time_spent
        
        # Contar pomodoros para esta tarea
        pomodoros_result = supabase.table("pomodoros").select("id").eq("task_id", task.id).eq("completed", True).execute()
        category_stats[category]["pomodoros_completed"] += len(pomodoros_result.data) if pomodoros_result.data else 0
        category_stats[category]["tasks_count"] += 1
    
    category_stats_list = [
        CategoryStats(
            category=cat,
            total_time_spent=stats["total_time_spent"],
            pomodoros_completed=stats["pomodoros_completed"],
            tasks_count=stats["tasks_count"]
        )
        for cat, stats in category_stats.items()
    ]
    
    # Obtener total de pomodoros completados
    total_pomodoros = PomodoroService.get_pomodoro_count(user_id=user_id)
    
    # Calcular tiempo total gastado (suma de todos los time_spent de tareas)
    total_time_spent = sum(task.time_spent for task in tasks)
    
    # Obtener estadísticas de distracciones
    distractions = DistractionService.get_all_distractions(user_id=user_id)
    distractions_count = len([d for d in distractions if d.had_distractions])
    phone_usage_count = len([d for d in distractions if d.used_phone])
    
    return StatisticsResponse(
        total_pomodoros=total_pomodoros,
        total_time_spent=total_time_spent,
        tasks_stats=tasks_stats,
        category_stats=category_stats_list,
        distractions_count=distractions_count,
        phone_usage_count=phone_usage_count
    )
