# DevPomodoro

Aplicación web de Pomodoro Timer diseñada para desarrolladores con gestión de tareas y subtareas.

## Características

- ⏱️ Timer Pomodoro con modos: Pomodoro, Short Break, Long Break
- 📋 Gestión de tareas con subtareas
- ⏲️ Cronometraje de tiempo por tarea y subtarea
- 🎯 Definición de objetivos para cada pomodoro
- 🔔 Modal de reflexión sobre distracciones (aparece aleatoriamente)
- 🎨 Interfaz oscura moderna estilo "for devs"

## Tecnologías

- React 18
- Vite
- CSS Variables para temas

## Instalación

```bash
yarn install
```

## Desarrollo

```bash
yarn dev
```

## Build

```bash
yarn build
```

## Preview

```bash
yarn preview
```

## Estructura del Proyecto

```
src/
  components/
    Header.jsx          # Barra superior con navegación
    TaskList.jsx        # Lista de tareas y subtareas
    PomodoroTimer.jsx   # Timer principal
    DistractionModal.jsx # Modal de reflexión
  App.jsx              # Componente principal
  main.jsx             # Punto de entrada
```
