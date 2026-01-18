# 🚀 Guía Rápida de Desarrollo

## Inicio Rápido

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy env.example .env
# Editar .env con tus credenciales de Supabase
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend disponible en**: `http://localhost:8000`
**Documentación API**: `http://localhost:8000/docs`

### 2. Frontend

```bash
cd frontend
yarn install
yarn dev
```

**Frontend disponible en**: `http://localhost:5173`

## Configuración de Conexión

### Backend → Frontend

El backend está configurado para aceptar peticiones desde el frontend mediante CORS:
- Configuración en: `backend/app/config.py`
- Variable de entorno: `CORS_ORIGINS=http://localhost:5173` (en `.env`)

### Frontend → Backend

El frontend se conecta al backend mediante:
1. **Proxy de Vite** (desarrollo): Configurado en `frontend/vite.config.js`
   - Redirige `/api/*` → `http://localhost:8000/api/*`
2. **Servicio API**: `frontend/src/services/api.js`
   - Proporciona funciones para todos los endpoints del backend

## Variables de Entorno

### Backend (`backend/.env`)
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-api-key-publica
CORS_ORIGINS=http://localhost:5173
ENVIRONMENT=development
DEBUG=True
```

### Frontend (`frontend/.env` - Opcional)
```env
VITE_API_URL=http://localhost:8000
```

**Nota**: Si no creas `.env` en el frontend, usará `http://localhost:8000` por defecto.

## Verificación de Conexión

1. **Backend funcionando**: Abre `http://localhost:8000/docs` en tu navegador
2. **Frontend funcionando**: Abre `http://localhost:5173` en tu navegador
3. **Conexión**: Abre la consola del navegador (F12) y verifica que no haya errores de CORS

## Estructura de Archivos Clave

```
backend/
├── app/
│   ├── main.py          # Configuración CORS y routers
│   └── config.py        # Settings con CORS_ORIGINS
└── .env                 # Variables de entorno

frontend/
├── src/
│   └── services/
│       └── api.js       # Cliente API completo
└── vite.config.js      # Proxy configurado
```

## Comandos Útiles

### Backend
```bash
# Ejecutar servidor
uvicorn app.main:app --reload

# Verificar salud del servidor
curl http://localhost:8000/health
```

### Frontend
```bash
# Desarrollo
yarn dev

# Build
yarn build

# Preview
yarn preview
```

## Solución de Problemas Comunes

### Error: "CORS policy"
- Verifica que `CORS_ORIGINS` en backend incluya `http://localhost:5173`
- Reinicia el servidor backend

### Error: "Failed to fetch"
- Verifica que el backend esté ejecutándose en el puerto 8000
- Verifica que no haya firewall bloqueando el puerto

### Variables de entorno no funcionan
- En frontend, deben comenzar con `VITE_`
- Reinicia el servidor después de cambiar `.env`
