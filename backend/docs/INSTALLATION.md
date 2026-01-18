# 📦 Guía de Instalación - MyPomodoro Backend

Esta guía te llevará paso a paso para instalar y configurar el backend de MyPomodoro.

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.9 o superior** - [Descargar Python](https://www.python.org/downloads/)
- **pip** (gestor de paquetes de Python) - Viene incluido con Python 3.4+
- **Git** (opcional) - [Descargar Git](https://git-scm.com/downloads)
- **Cuenta en Supabase** - [Crear cuenta gratuita](https://supabase.com/)

---

## 🔧 Paso 1: Clonar/Preparar el Proyecto

### Opción A: Si tienes el proyecto en Git
```bash
git clone <url-del-repositorio>
cd mypomodoro/backend
```

### Opción B: Si ya tienes los archivos
```bash
cd mypomodoro/backend
```

---

## 🐍 Paso 2: Crear Entorno Virtual (Recomendado)

Crear un entorno virtual aísla las dependencias del proyecto.

### En Windows (PowerShell o CMD):
```bash
python -m venv venv

# Activar el entorno virtual
venv\Scripts\activate
```

### En Linux/Mac:
```bash
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

**Nota**: Una vez activado, verás `(venv)` al inicio de tu línea de comandos.

---

## 📥 Paso 3: Instalar Dependencias

Con el entorno virtual activado, instala las dependencias:

```bash
pip install -r requirements.txt
```

Esto instalará:
- FastAPI
- Uvicorn (servidor ASGI)
- Supabase (cliente para Supabase)
- Pydantic (validación de datos)
- Y otras dependencias necesarias

**Verificación**: Verifica la instalación ejecutando:
```bash
pip list
```

Deberías ver todas las dependencias listadas.

---

## 🗄️ Paso 4: Configurar Supabase

### 4.1 Crear Proyecto en Supabase

1. Ve a [supabase.com](https://supabase.com/) e inicia sesión
2. Haz clic en **"New Project"**
3. Completa los campos:
   - **Name**: `mypomodoro` (o el nombre que prefieras)
   - **Database Password**: Crea una contraseña segura (guárdala)
   - **Region**: Selecciona la región más cercana
4. Haz clic en **"Create new project"**
5. Espera a que se cree el proyecto (2-3 minutos)

### 4.2 Obtener Credenciales de Supabase

1. En tu proyecto de Supabase, ve a **Settings** (⚙️) en el menú lateral
2. Selecciona **API** en el submenú
3. Copia los siguientes valores:
   - **Project URL** (ejemplo: `https://xxxxx.supabase.co`)
   - **anon public** key (una clave larga que empieza con `eyJ...`)

Guarda estos valores, los necesitarás en el siguiente paso.

### 4.3 Crear las Tablas en Supabase

1. En Supabase, ve a **SQL Editor** en el menú lateral
2. Haz clic en **"New query"**
3. Abre el archivo `docs/database/schema.sql` en tu editor de código
4. Copia **TODO** el contenido del archivo
5. Pega el contenido en el SQL Editor de Supabase
6. Haz clic en **"Run"** (o presiona `Ctrl + Enter`)

**Verificación**: Deberías ver un mensaje de éxito. Para verificar que las tablas se crearon:
- Ve a **Table Editor** en el menú lateral
- Deberías ver 4 tablas: `tasks`, `subtasks`, `pomodoros`, `distractions`

---

## ⚙️ Paso 5: Configurar Variables de Entorno

1. En la raíz del proyecto `backend/`, crea un archivo llamado `.env`

### En Windows (PowerShell):
```bash
copy env.example .env
```

### En Linux/Mac:
```bash
cp env.example .env
```

2. Abre el archivo `.env` con tu editor de código

3. Completa los valores:

```env
# Configuración de Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-api-key-publica-de-supabase

# Opcional: Service Key para operaciones administrativas
# SUPABASE_SERVICE_KEY=tu-service-key-privada

# Configuración de CORS (separar múltiples orígenes con comas)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Ambiente
ENVIRONMENT=development
DEBUG=True
```

**Importante**:
- Reemplaza `https://tu-proyecto.supabase.co` con tu **Project URL** de Supabase
- Reemplaza `tu-api-key-publica-de-supabase` con tu **anon public** key
- Ajusta `CORS_ORIGINS` si tu frontend corre en otro puerto

**Ejemplo completo**:
```env
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY0NzUwNzI5MCwiZXhwIjoxOTYzMDgzMjkwfQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
DEBUG=True
```

---

## 🚀 Paso 6: Ejecutar el Servidor

Con todo configurado, puedes iniciar el servidor:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Explicación de los parámetros**:
- `--reload`: Recarga automática cuando cambies código (solo desarrollo)
- `--host 0.0.0.0`: Permite acceso desde cualquier IP
- `--port 8000`: Puerto donde correrá el servidor

**Verificación**: Deberías ver un mensaje como:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## ✅ Paso 7: Verificar que Todo Funciona

### 7.1 Verificar Endpoint de Salud

Abre tu navegador o usa curl:

```bash
curl http://localhost:8000/health
```

Deberías ver:
```json
{"status": "healthy"}
```

### 7.2 Ver Documentación Interactiva

Abre en tu navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Aquí puedes ver todos los endpoints disponibles y probarlos directamente.

### 7.3 Probar un Endpoint

Desde Swagger UI (`/docs`):
1. Expande el endpoint `POST /api/v1/tasks/`
2. Haz clic en **"Try it out"**
3. Edita el JSON de ejemplo:
```json
{
  "title": "Tarea de prueba",
  "category": "personal"
}
```
4. Haz clic en **"Execute"**
5. Deberías ver una respuesta 201 con la tarea creada

---

## 🐛 Solución de Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solución**: Asegúrate de que el entorno virtual esté activado y las dependencias instaladas:
```bash
# Verificar que venv está activo (debería aparecer (venv))
pip install -r requirements.txt
```

### Error: "SUPABASE_URL not found" o "SUPABASE_KEY not found"

**Solución**: 
1. Verifica que el archivo `.env` existe en la raíz del proyecto `backend/`
2. Verifica que tiene las variables `SUPABASE_URL` y `SUPABASE_KEY`
3. Asegúrate de que no haya espacios alrededor del `=` en el `.env`

### Error de conexión a Supabase

**Solución**:
1. Verifica que `SUPABASE_URL` y `SUPABASE_KEY` sean correctos
2. Asegúrate de copiar el **anon public** key, no la service_role key
3. Verifica que tu proyecto de Supabase esté activo

### Error al ejecutar SQL en Supabase

**Solución**:
1. Verifica que tienes permisos en el proyecto
2. Asegúrate de ejecutar el script completo desde `docs/database/schema.sql`
3. Si hay errores de "already exists", las tablas ya están creadas (puedes continuar)

### Error de CORS en el frontend

**Solución**:
1. Verifica que `CORS_ORIGINS` en `.env` incluya la URL exacta de tu frontend
2. Reinicia el servidor después de cambiar `.env`
3. Asegúrate de que no haya espacios en `CORS_ORIGINS`

### Puerto 8000 ya está en uso

**Solución**: Usa otro puerto:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

---

## 📚 Siguientes Pasos

Una vez que el backend esté funcionando:

1. **Integrar con el frontend**: Configura el frontend para apuntar a `http://localhost:8000`
2. **Revisar la documentación API**: Explora `/docs` para ver todos los endpoints
3. **Leer el README principal**: `README.md` para más información sobre la estructura del proyecto
4. **Revisar el esquema de BD**: `docs/database/schema.md` para entender la estructura de datos

---

## 💡 Consejos Adicionales

### Desarrollo

- Usa `--reload` solo en desarrollo
- El modo reload detecta cambios automáticamente
- Los logs aparecen en la consola

### Producción

Para producción, usa:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Variables de Entorno

Nunca commitees el archivo `.env` a Git (ya está en `.gitignore`). Para producción:
- Usa variables de entorno del sistema
- O un servicio de gestión de secrets (AWS Secrets Manager, etc.)

---

## 📞 ¿Necesitas Ayuda?

Si encuentras problemas:

1. Revisa la sección de **Solución de Problemas** arriba
2. Verifica los logs del servidor para mensajes de error
3. Consulta la documentación de [FastAPI](https://fastapi.tiangolo.com/)
4. Consulta la documentación de [Supabase](https://supabase.com/docs)

---

**¡Felicitaciones! 🎉 Tu backend de MyPomodoro está listo para usar.**
