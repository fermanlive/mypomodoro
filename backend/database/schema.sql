-- MyPomodoro Database Schema para Supabase
-- Este archivo contiene todas las tablas necesarias para la aplicación

-- Tabla de Usuarios (puede extenderse con autenticación de Supabase Auth)
-- Por ahora, solo guardamos user_id como string para futuras integraciones

-- Tabla de Tareas
CREATE TABLE IF NOT EXISTS tasks (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    category VARCHAR(20) DEFAULT 'personal' NOT NULL CHECK (category IN ('personal', 'laboral', 'otro')),
    custom_category VARCHAR(100),
    time_spent INTEGER DEFAULT 0 NOT NULL, -- En segundos
    user_id VARCHAR(255), -- Para multi-usuario (puede ser UUID de Supabase Auth)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Índices para tareas
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at DESC);

-- Tabla de Subtareas
CREATE TABLE IF NOT EXISTS subtasks (
    id BIGSERIAL PRIMARY KEY,
    task_id BIGINT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    time_spent INTEGER DEFAULT 0 NOT NULL, -- En segundos
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Índices para subtareas
CREATE INDEX IF NOT EXISTS idx_subtasks_task_id ON subtasks(task_id);
CREATE INDEX IF NOT EXISTS idx_subtasks_completed ON subtasks(completed);

-- Tabla de Pomodoros
CREATE TABLE IF NOT EXISTS pomodoros (
    id BIGSERIAL PRIMARY KEY,
    mode VARCHAR(20) DEFAULT 'pomodoro' NOT NULL CHECK (mode IN ('pomodoro', 'shortBreak', 'longBreak')),
    objective TEXT,
    task_id BIGINT REFERENCES tasks(id) ON DELETE SET NULL,
    subtask_ids BIGINT[], -- Array de IDs de subtareas
    duration INTEGER DEFAULT 1500 NOT NULL, -- Duración en segundos (25 min por defecto)
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    user_id VARCHAR(255), -- Para multi-usuario
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Índices para pomodoros
CREATE INDEX IF NOT EXISTS idx_pomodoros_user_id ON pomodoros(user_id);
CREATE INDEX IF NOT EXISTS idx_pomodoros_completed ON pomodoros(completed);
CREATE INDEX IF NOT EXISTS idx_pomodoros_mode ON pomodoros(mode);
CREATE INDEX IF NOT EXISTS idx_pomodoros_task_id ON pomodoros(task_id);
CREATE INDEX IF NOT EXISTS idx_pomodoros_created_at ON pomodoros(created_at DESC);

-- Tabla de Distracciones
CREATE TABLE IF NOT EXISTS distractions (
    id BIGSERIAL PRIMARY KEY,
    pomodoro_id BIGINT NOT NULL REFERENCES pomodoros(id) ON DELETE CASCADE,
    had_distractions BOOLEAN NOT NULL,
    used_phone BOOLEAN NOT NULL,
    user_id VARCHAR(255), -- Para multi-usuario
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Índices para distracciones
CREATE INDEX IF NOT EXISTS idx_distractions_pomodoro_id ON distractions(pomodoro_id);
CREATE INDEX IF NOT EXISTS idx_distractions_user_id ON distractions(user_id);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para actualizar updated_at
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subtasks_updated_at BEFORE UPDATE ON subtasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pomodoros_updated_at BEFORE UPDATE ON pomodoros
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función para actualizar time_spent de la tarea cuando se actualiza una subtarea
CREATE OR REPLACE FUNCTION update_task_time_spent()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE tasks
    SET time_spent = (
        SELECT COALESCE(SUM(time_spent), 0)
        FROM subtasks
        WHERE task_id = COALESCE(NEW.task_id, OLD.task_id)
    )
    WHERE id = COALESCE(NEW.task_id, OLD.task_id);
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar time_spent cuando cambia time_spent de una subtarea
CREATE TRIGGER update_task_time_on_subtask_time_change
    AFTER INSERT OR UPDATE OF time_spent OR DELETE ON subtasks
    FOR EACH ROW EXECUTE FUNCTION update_task_time_spent();

-- Función para marcar tarea como completada si todas las subtareas están completadas
CREATE OR REPLACE FUNCTION check_task_completion()
RETURNS TRIGGER AS $$
DECLARE
    all_completed BOOLEAN;
    subtask_count INTEGER;
BEGIN
    -- Contar subtareas
    SELECT COUNT(*) INTO subtask_count
    FROM subtasks
    WHERE task_id = COALESCE(NEW.task_id, OLD.task_id);
    
    -- Si no hay subtareas, no hacer nada
    IF subtask_count = 0 THEN
        RETURN NEW;
    END IF;
    
    -- Verificar si todas están completadas
    SELECT COUNT(*) = COUNT(*) FILTER (WHERE completed = TRUE) INTO all_completed
    FROM subtasks
    WHERE task_id = COALESCE(NEW.task_id, OLD.task_id);
    
    -- Actualizar estado de la tarea
    UPDATE tasks
    SET completed = all_completed
    WHERE id = COALESCE(NEW.task_id, OLD.task_id);
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar completed cuando cambia el estado de una subtarea
CREATE TRIGGER check_task_completion_on_subtask_change
    AFTER INSERT OR UPDATE OF completed OR DELETE ON subtasks
    FOR EACH ROW EXECUTE FUNCTION check_task_completion();

-- Comentarios en las tablas (documentación)
COMMENT ON TABLE tasks IS 'Tabla principal de tareas del usuario';
COMMENT ON TABLE subtasks IS 'Subtareas asociadas a las tareas';
COMMENT ON TABLE pomodoros IS 'Registro de sesiones de pomodoro completadas';
COMMENT ON TABLE distractions IS 'Registro de distracciones durante pomodoros';

COMMENT ON COLUMN tasks.time_spent IS 'Tiempo total gastado en segundos (suma de subtareas)';
COMMENT ON COLUMN subtasks.time_spent IS 'Tiempo gastado en esta subtarea en segundos';
COMMENT ON COLUMN pomodoros.duration IS 'Duración del pomodoro en segundos';
COMMENT ON COLUMN pomodoros.subtask_ids IS 'Array de IDs de subtareas asociadas al pomodoro';
