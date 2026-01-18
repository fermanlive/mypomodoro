-- MyPomodoro - Mock Users for Testing
-- Este archivo contiene datos de prueba de usuarios para testing
-- Estos user_id pueden ser UUIDs de Supabase Auth o cualquier identificador único

-- Tabla de referencia de usuarios de prueba (opcional, para documentación)
-- Si deseas crear una tabla real de usuarios, descomenta la siguiente sección:
/*
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
*/

-- UUIDs de usuarios de prueba (formato típico de Supabase Auth)
-- User 1: Juan Pérez
-- User 2: María García
-- User 3: Carlos López
-- User 4: Ana Martínez
-- User 5: Test User (para pruebas generales)

-- Datos de prueba para TASKS asociados a usuarios
INSERT INTO tasks (id, title, category, completed, time_spent, user_id, created_at, updated_at) VALUES
-- Usuario 1: 550e8400-e29b-41d4-a716-446655440001
(1, 'Implementar autenticación', 'laboral', false, 0, '550e8400-e29b-41d4-a716-446655440001', NOW(), NOW()),
(2, 'Revisar código de tests', 'laboral', true, 1800, '550e8400-e29b-41d4-a716-446655440001', NOW(), NOW()),
(3, 'Hacer ejercicio', 'personal', false, 0, '550e8400-e29b-41d4-a716-446655440001', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),

-- Usuario 2: 550e8400-e29b-41d4-a716-446655440002
(4, 'Diseñar interfaz de usuario', 'laboral', false, 900, '550e8400-e29b-41d4-a716-446655440002', NOW(), NOW()),
(5, 'Comprar groceries', 'personal', true, 0, '550e8400-e29b-41d4-a716-446655440002', NOW() - INTERVAL '1 days', NOW() - INTERVAL '1 days'),

-- Usuario 3: 550e8400-e29b-41d4-a716-446655440003
(6, 'Escribir documentación', 'laboral', false, 2700, '550e8400-e29b-41d4-a716-446655440003', NOW(), NOW()),
(7, 'Llamar al dentista', 'personal', false, 0, '550e8400-e29b-41d4-a716-446655440003', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),

-- Usuario 4: 550e8400-e29b-41d4-a716-446655440004
(8, 'Configurar CI/CD', 'laboral', false, 3600, '550e8400-e29b-41d4-a716-446655440004', NOW(), NOW()),
(9, 'Leer un libro', 'personal', false, 1200, '550e8400-e29b-41d4-a716-446655440004', NOW() - INTERVAL '1 days', NOW() - INTERVAL '1 days'),

-- Usuario test: 00000000-0000-0000-0000-000000000000
(10, 'Test Task 1', 'personal', false, 0, '00000000-0000-0000-0000-000000000000', NOW(), NOW()),
(11, 'Test Task 2', 'laboral', true, 1500, '00000000-0000-0000-0000-000000000000', NOW(), NOW());

-- Datos de prueba para SUBTASKS
INSERT INTO subtasks (id, task_id, title, completed, time_spent, created_at, updated_at) VALUES
-- Subtareas de la tarea 1 (Usuario 1)
(1, 1, 'Investigar JWT tokens', false, 600, NOW(), NOW()),
(2, 1, 'Implementar login endpoint', false, 400, NOW(), NOW()),
(3, 1, 'Escribir tests de autenticación', false, 0, NOW(), NOW()),

-- Subtareas de la tarea 2 (Usuario 1)
(4, 2, 'Revisar test_task_service.py', true, 900, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
(5, 2, 'Revisar test_pomodoro_service.py', true, 900, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),

-- Subtareas de la tarea 4 (Usuario 2)
(6, 4, 'Crear wireframes', true, 600, NOW(), NOW()),
(7, 4, 'Seleccionar paleta de colores', false, 300, NOW(), NOW()),

-- Subtareas de la tarea 6 (Usuario 3)
(8, 6, 'Documentar API endpoints', false, 1800, NOW(), NOW()),
(9, 6, 'Documentar esquema de base de datos', false, 900, NOW(), NOW()),

-- Subtareas de la tarea 8 (Usuario 4)
(10, 8, 'Configurar GitHub Actions', false, 2400, NOW(), NOW()),
(11, 8, 'Configurar pipeline de tests', true, 1200, NOW(), NOW());

-- Datos de prueba para POMODOROS
INSERT INTO pomodoros (id, mode, objective, task_id, duration, completed, started_at, completed_at, user_id, created_at, updated_at) VALUES
-- Pomodoros del Usuario 1
(1, 'pomodoro', 'Trabajar en autenticación', 1, 1500, true, NOW() - INTERVAL '2 hours', NOW() - INTERVAL '1.5 hours', '550e8400-e29b-41d4-a716-446655440001', NOW() - INTERVAL '2 hours', NOW() - INTERVAL '1.5 hours'),
(2, 'shortBreak', NULL, NULL, 300, true, NOW() - INTERVAL '1.5 hours', NOW() - INTERVAL '1.25 hours', '550e8400-e29b-41d4-a716-446655440001', NOW() - INTERVAL '1.5 hours', NOW() - INTERVAL '1.25 hours'),
(3, 'pomodoro', 'Revisar tests', 2, 1500, true, NOW() - INTERVAL '1 hour', NOW(), '550e8400-e29b-41d4-a716-446655440001', NOW() - INTERVAL '1 hour', NOW()),

-- Pomodoros del Usuario 2
(4, 'pomodoro', 'Diseñar UI mockups', 4, 1500, true, NOW() - INTERVAL '30 minutes', NOW() - INTERVAL '15 minutes', '550e8400-e29b-41d4-a716-446655440002', NOW() - INTERVAL '30 minutes', NOW() - INTERVAL '15 minutes'),
(5, 'longBreak', NULL, NULL, 900, true, NOW() - INTERVAL '15 minutes', NOW(), '550e8400-e29b-41d4-a716-446655440002', NOW() - INTERVAL '15 minutes', NOW()),

-- Pomodoros del Usuario 3
(6, 'pomodoro', 'Documentar API', 6, 1500, false, NOW() - INTERVAL '20 minutes', NULL, '550e8400-e29b-41d4-a716-446655440003', NOW() - INTERVAL '20 minutes', NOW() - INTERVAL '20 minutes'),

-- Pomodoros del Usuario 4
(7, 'pomodoro', 'Configurar CI/CD', 8, 1500, true, NOW() - INTERVAL '2 days', NOW() - INTERVAL '1.9 days', '550e8400-e29b-41d4-a716-446655440004', NOW() - INTERVAL '2 days', NOW() - INTERVAL '1.9 days'),
(8, 'pomodoro', 'Leer', 9, 1500, false, NOW() - INTERVAL '1 hour', NULL, '550e8400-e29b-41d4-a716-446655440004', NOW() - INTERVAL '1 hour', NOW() - INTERVAL '1 hour');

-- Datos de prueba para DISTRACTIONS
INSERT INTO distractions (id, pomodoro_id, had_distractions, used_phone, user_id, created_at) VALUES
-- Distracciones Usuario 1
(1, 1, false, false, '550e8400-e29b-41d4-a716-446655440001', NOW() - INTERVAL '2 hours'),
(2, 3, true, true, '550e8400-e29b-41d4-a716-446655440001', NOW() - INTERVAL '1 hour'),

-- Distracciones Usuario 2
(3, 4, false, false, '550e8400-e29b-41d4-a716-446655440002', NOW() - INTERVAL '30 minutes'),

-- Distracciones Usuario 4
(4, 7, true, false, '550e8400-e29b-41d4-a716-446655440004', NOW() - INTERVAL '2 days');

-- Comentarios con los UUIDs de prueba
/*
========== USER IDS DE PRUEBA ==========

Los siguientes user_id se utilizan en los datos de prueba:

1. Juan Pérez (Developer)
   UUID: 550e8400-e29b-41d4-a716-446655440001

2. María García (Designer)
   UUID: 550e8400-e29b-41d4-a716-446655440002

3. Carlos López (Technical Writer)
   UUID: 550e8400-e29b-41d4-a716-446655440003

4. Ana Martínez (DevOps)
   UUID: 550e8400-e29b-41d4-a716-446655440004

5. Test User (Propósito general de testing)
   UUID: 00000000-0000-0000-0000-000000000000

========== CÓMO USAR ESTOS DATOS ==========

1. Para ejecutar este script en Supabase:
   - Ve a la consola SQL de Supabase
   - Copia y pega el contenido de este archivo
   - Ejecuta el script

2. Alternativa con psql (en local):
   psql -U postgres -d your_database -f mocks_users.sql

3. Para limpiar los datos de prueba, ejecuta:
   DELETE FROM distractions;
   DELETE FROM pomodoros;
   DELETE FROM subtasks;
   DELETE FROM tasks;
   
   (Este comando respeta los ON DELETE CASCADE definidos)

========== QUERIES ÚTILES PARA TESTING ==========

-- Ver todas las tareas de un usuario
SELECT * FROM tasks WHERE user_id = '550e8400-e29b-41d4-a716-446655440001' ORDER BY created_at DESC;

-- Ver todas las tareas completadas de un usuario
SELECT * FROM tasks WHERE user_id = '550e8400-e29b-41d4-a716-446655440001' AND completed = true;

-- Ver estadísticas de pomodoros por usuario
SELECT 
    user_id,
    COUNT(*) as total_pomodoros,
    COUNT(*) FILTER (WHERE completed = true) as completed_pomodoros,
    COUNT(*) FILTER (WHERE mode = 'pomodoro') as pomodoro_sessions,
    ROUND(AVG(EXTRACT(EPOCH FROM (completed_at - started_at))/60), 2) as avg_duration_minutes
FROM pomodoros
WHERE user_id = '550e8400-e29b-41d4-a716-446655440001'
GROUP BY user_id;

-- Ver distracciones registradas
SELECT 
    p.user_id,
    COUNT(*) as total_distractions,
    COUNT(*) FILTER (WHERE had_distractions = true) as distractions_count,
    COUNT(*) FILTER (WHERE used_phone = true) as phone_usage_count
FROM distractions d
JOIN pomodoros p ON d.pomodoro_id = p.id
GROUP BY p.user_id;

-- Ver progreso de subtareas
SELECT 
    t.user_id,
    t.title,
    COUNT(*) as total_subtasks,
    COUNT(*) FILTER (WHERE completed = true) as completed_subtasks
FROM subtasks s
JOIN tasks t ON s.task_id = t.id
WHERE t.user_id = '550e8400-e29b-41d4-a716-446655440001'
GROUP BY t.id, t.title, t.user_id;

*/
