# Funcionalidades de DevPomodoro

Este documento describe todas las funcionalidades implementadas en la aplicación DevPomodoro para que otro agente pueda continuar el desarrollo o realizar modificaciones.

## 📋 Estructura General

DevPomodoro es una aplicación web de gestión de tiempo tipo Pomodoro diseñada específicamente para desarrolladores, con un diseño oscuro moderno y funcionalidades avanzadas de gestión de tareas.

---

## 🎯 Funcionalidades Principales

### 1. Sistema de Pomodoro Timer

**Ubicación**: `src/components/PomodoroTimer.jsx`

**Características**:
- **Tres modos de temporizador**:
  - Pomodoro: 25 minutos (modo por defecto)
  - Short Break: 5 minutos
  - Long Break: 15 minutos
- **Controles**:
  - Botón START para iniciar el temporizador
  - Botón PAUSE para pausar (se muestra cuando está corriendo)
  - Cambio automático de modo al seleccionar otro
- **Display visual**:
  - Círculo grande con tiempo restante en formato MM:SS
  - Contador de pomodoros (#1, #2, etc.)
  - Mensaje motivacional "Time to code!"

**Estado del Pomodoro** (en `src/App.jsx`):
- `timer`: tiempo restante en segundos
- `isRunning`: boolean indicando si está corriendo
- `mode`: 'pomodoro', 'shortBreak', 'longBreak'
- `objective`: texto del objetivo del pomodoro actual
- `taskId`: ID de la tarea asociada (opcional)
- `subtaskIds`: Array de IDs de subtareas asociadas (opcional)

**Funcionalidad especial**:
- Cuando un pomodoro se completa (solo en modo 'pomodoro'), se actualiza automáticamente el tiempo gastado en las tareas/subtareas asociadas
- Se incrementa el contador global de pomodoros completados

---

### 2. Gestión de Tareas y Subtareas

**Ubicación**: `src/components/TaskList.jsx`

#### 2.1 Estructura de Tareas

Cada tarea tiene la siguiente estructura:
```javascript
{
  id: Number,
  title: String,
  completed: Boolean,
  category: 'personal' | 'laboral' | 'otro',
  customCategory: String, // Solo usado si category === 'otro'
  subtasks: Array<Subtask>,
  timeSpent: Number // En segundos (suma de todas las subtareas)
}
```

Cada subtarea:
```javascript
{
  id: Number,
  title: String,
  completed: Boolean,
  timeSpent: Number // En segundos
}
```

#### 2.2 Funcionalidades de Tareas

- **Crear tarea**: Botón "+ Add Task" en la parte inferior
- **Editar título**: Doble clic en el título de la tarea
- **Completar tarea**: Checkbox en la tarea
  - Si todas las subtareas están completas, la tarea se marca como completada automáticamente
- **Expandir/Colapsar**: Clic en el área de contenido de la tarea
- **Eliminar tarea**: Menú de puntos suspensivos (⋯) → "Eliminar"
- **Archivar tarea**: Menú de puntos suspensivos (⋯) → "Archivar" (actualmente elimina la tarea)

#### 2.3 Funcionalidades de Subtareas

- **Agregar subtarea**: Botón "+ Add Subtask" dentro de una tarea expandida
- **Completar subtarea**: Checkbox individual
- **Seleccionar subtarea para Pomodoro**: Botón "Seleccionar" en cada subtarea
- **Seleccionar todas las subtareas**: Botón "Seleccionar todas" (aparece si hay 2+ subtareas)
- **Visualización de tiempo**: Muestra tiempo acumulado en formato "Xm" o "Xh Xm"

#### 2.4 Categorías de Tareas

- **Selector de categoría**: Dropdown con opciones:
  - Personal
  - Laboral
  - Otro
- **Categoría personalizada**: Si se selecciona "Otro", aparece un input para definir el nombre personalizado
- **Ubicación**: Se muestra en la sección expandida de la tarea, antes de la barra de progreso

#### 2.5 Barra de Progreso

- Muestra el porcentaje de completitud basado en subtareas completadas
- Se actualiza automáticamente cuando se completa/marca una subtarea

#### 2.6 Búsqueda de Tareas

- Campo de búsqueda en el header de la lista de tareas
- Filtra por título de tarea (case-insensitive)
- Búsqueda en tiempo real mientras se escribe

---

### 3. Campo de Objetivo del Pomodoro

**Ubicación**: `src/components/PomodoroTimer.jsx`

**Características**:
- Texto: "En este pomodoro deseo terminar:"
- **Modo visualización**: Muestra el objetivo actual o el nombre de la tarea/subtareas seleccionadas
- **Modo edición**: 
  - Botón "Edit" para activar edición
  - Input de texto para escribir objetivo personalizado
  - Enter o blur para guardar
  - Botón ✓ para confirmar
- **Integración con tareas**: Si hay una tarea seleccionada, muestra automáticamente el nombre de la tarea y subtareas

---

### 4. Modal de Reflexión sobre Distracciones

**Ubicación**: `src/components/DistractionModal.jsx`

**Características**:
- **Aparición aleatoria**: 
  - Se muestra 3 veces cada 10 pomodoros completados
  - Probabilidad ajustada dinámicamente para garantizar exactamente 3 apariciones por cada grupo de 10
  - Solo aparece después de completar un pomodoro (no después de breaks)
- **Preguntas**:
  1. "¿El anterior pomodoro tuviste distracciones?" (Sí/No)
  2. "¿Usaste el celular en el último pomodoro?" (Sí/No)
- **Interacción**:
  - Botones de respuesta destacados visualmente
  - Botón "Guardar" para cerrar el modal
  - Botón "×" para cerrar
  - Los datos se registran en consola (se puede extender para backend)

**Lógica de aparición** (en `src/App.jsx`):
- Se controla mediante `pomodoroCount` y `distractionModalShown`
- Garantiza distribución equitativa dentro de cada grupo de 10 pomodoros

---

### 5. Integración Tareas-Pomodoro

**Funcionalidad**:
- Desde la lista de tareas, se pueden seleccionar subtareas individuales o todas las subtareas de una tarea
- Al seleccionar, se actualiza `currentPomodoro` con:
  - `taskId`: ID de la tarea
  - `subtaskIds`: Array de IDs de subtareas seleccionadas
- Cuando se completa un pomodoro:
  - Se suma 25 minutos (1500 segundos) al tiempo de cada subtarea seleccionada
  - Se actualiza el tiempo total de la tarea (suma de todas las subtareas)
- El objetivo del pomodoro se actualiza automáticamente con el nombre de las tareas/subtareas seleccionadas

---

### 6. Diseño y Estilos

**Tema oscuro "for devs"**:
- **Colores principales**:
  - Fondo primario: `#0d1117`
  - Fondo secundario: `#161b22`
  - Fondo terciario: `#21262d`
  - Borde: `#30363d`
  - Texto primario: `#c9d1d9`
  - Texto secundario: `#8b949e`
  - Acento verde: `#3fb950`
  - Acento rojo: `#f85149`
  - Acento azul: `#58a6ff`
- **Fuente**: Fira Code (monospace, estilo código)
- **Componentes visuales**:
  - Header con navegación (Report, Settings, Sign In)
  - Lista de tareas a la izquierda (400px)
  - Timer Pomodoro centrado a la derecha
  - Menús desplegables con sombras y bordes

**CSS Variables**: Todas las variables de color están en `src/index.css` bajo `:root`

---

## 🗂️ Estructura de Archivos

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Barra superior
│   │   ├── Header.css
│   │   ├── TaskList.jsx        # Lista de tareas completa
│   │   ├── TaskList.css
│   │   ├── PomodoroTimer.jsx   # Timer principal
│   │   ├── PomodoroTimer.css
│   │   ├── DistractionModal.jsx # Modal de distracciones
│   │   └── DistractionModal.css
│   ├── App.jsx                 # Componente principal (lógica de estado)
│   ├── App.css
│   ├── main.jsx                # Punto de entrada
│   └── index.css               # Estilos globales y variables CSS
├── index.html                  # HTML principal
├── vite.config.js              # Configuración de Vite
├── package.json                # Dependencias y scripts
└── README.md                   # Documentación del proyecto
```

---

## 🔄 Flujo de Datos

### Estado Principal (App.jsx)
- `tasks`: Array de todas las tareas
- `currentPomodoro`: Estado actual del pomodoro
- `pomodoroCount`: Contador de pomodoros completados
- `showDistractionModal`: Boolean para mostrar/ocultar modal
- `distractionModalShown`: Array de pomodoros donde ya se mostró el modal

### Actualización de Estado
- `onTasksChange`: Callback para actualizar el array de tareas
- `onCurrentPomodoroChange`: Callback para actualizar el pomodoro actual
- `onPomodoroComplete`: Se ejecuta cuando un pomodoro termina, actualiza tiempos y contador

---

## 🎨 Componentes Clave

### TaskList Component
**Props**:
- `tasks`: Array de tareas
- `onTasksChange`: Función para actualizar tareas
- `currentPomodoro`: Estado del pomodoro actual
- `onCurrentPomodoroChange`: Función para actualizar pomodoro

**Estado interno**:
- `searchQuery`: Texto de búsqueda
- `editingTask`: ID de tarea en edición (o null)
- `expandedTasks`: Set de IDs de tareas expandidas
- `openMenuId`: ID de tarea con menú abierto (o null)

### PomodoroTimer Component
**Props**:
- `currentPomodoro`: Estado del pomodoro
- `onCurrentPomodoroChange`: Función para actualizar
- `tasks`: Array de tareas (para mostrar nombre de tarea seleccionada)
- `onPomodoroComplete`: Callback cuando termina

**Estado interno**:
- `timer`: Tiempo restante en segundos
- `isRunning`: Boolean
- `mode`: Modo actual
- `objective`: Texto del objetivo
- `editingObjective`: Boolean para modo edición
- `pomodoroNumber`: Número de pomodoro actual (se puede sincronizar con pomodoroCount)

---

## 🚀 Funcionalidades Futuras Sugeridas

1. **Persistencia de datos**: LocalStorage o backend para guardar tareas
2. **Estadísticas**: Reporte de tiempo por categoría, tarea, etc.
3. **Filtros**: Filtrar tareas por categoría, completadas, etc.
4. **Arrastrar y soltar**: Reordenar tareas/subtareas
5. **Notificaciones**: Notificar cuando termine un pomodoro
6. **Sonidos**: Sonido al completar pomodoro/break
7. **Temas**: Múltiples temas (aunque ya está preparado con CSS variables)
8. **Exportar/Importar**: Backup de tareas
9. **Colaboración**: Compartir tareas entre usuarios
10. **Historial de pomodoros**: Ver pomodoros anteriores y tiempos

---

## 📝 Notas Técnicas

- **Gestión de tiempo**: Todo el tiempo se maneja en segundos
- **IDs**: Se usa `Date.now()` para generar IDs únicos (en producción usar UUID)
- **Confirmación de eliminación**: Se usa `window.confirm()` (se puede mejorar con modal personalizado)
- **Cronometraje**: El timer usa `setInterval` con actualización cada segundo
- **React Hooks**: Se usa `useState` y `useEffect` para gestión de estado
- **Sin backend**: Todo es frontend puro, estado local en React
- **Sin enrutamiento**: Aplicación de una sola página (SPA)

---

## 🔧 Dependencias Principales

- **React 18.2.0**: Framework principal
- **Vite 5.0.8**: Build tool y dev server
- **@vitejs/plugin-react**: Plugin de Vite para React
- **@types/react**: Tipos TypeScript para React (aunque no se usa TS aún)

---

## 🎯 Comandos Principales

```bash
# Desarrollo
yarn dev

# Build para producción
yarn build

# Preview de build
yarn preview
```

---

## 📋 Checklist de Funcionalidades Implementadas

- ✅ Timer Pomodoro con 3 modos
- ✅ Gestión completa de tareas
- ✅ Gestión completa de subtareas
- ✅ Cronometraje por tarea/subtarea
- ✅ Categorías de tareas (Personal, Laboral, Otro)
- ✅ Categoría personalizada cuando es "Otro"
- ✅ Búsqueda de tareas
- ✅ Selección de tareas para pomodoro
- ✅ Modal de distracciones aleatorio
- ✅ Campo de objetivo del pomodoro
- ✅ Menú de acciones (Archivar, Eliminar)
- ✅ Barra de progreso por tarea
- ✅ Diseño oscuro estilo "for devs"
- ✅ Fuente Fira Code
- ✅ Responsive (parcialmente, puede mejorarse)

---

*Última actualización: Migración a Yarn*
