# 🧪 Tests Unitarios - MyPomodoro Backend

Documentación sobre las pruebas unitarias del proyecto.

## 📋 Estructura de Tests

```
tests/
├── __init__.py
├── conftest.py              # Configuración global y fixtures
├── test_task_service.py     # Tests para TaskService
├── test_subtask_service.py  # Tests para SubtaskService
├── test_pomodoro_service.py # Tests para PomodoroService
├── test_distraction_service.py # Tests para DistractionService
└── test_routers.py          # Tests para endpoints API
```

## 🚀 Ejecutar Tests

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar con coverage (cobertura de código)

```bash
pytest --cov=app --cov-report=html
```

Esto genera un reporte HTML en `htmlcov/index.html`

### Ejecutar tests específicos

```bash
# Un archivo específico
pytest tests/test_task_service.py

# Una clase específica
pytest tests/test_task_service.py::TestTaskService

# Un test específico
pytest tests/test_task_service.py::TestTaskService::test_create_task_success
```

### Ejecutar en modo verbose (detallado)

```bash
pytest -v
```

### Ejecutar solo tests que fallaron

```bash
pytest --lf  # last-failed
```

## 📊 Cobertura de Código

Para ver la cobertura de código:

```bash
pytest --cov=app --cov-report=term-missing
```

Esto muestra:
- Porcentaje de cobertura por módulo
- Líneas no cubiertas por tests

### Generar reporte HTML de cobertura

```bash
pytest --cov=app --cov-report=html
```

Luego abre `htmlcov/index.html` en tu navegador.

## 🧩 Fixtures Disponibles

Las fixtures están definidas en `conftest.py`:

- `client`: Cliente de prueba para FastAPI (TestClient)
- `mock_supabase`: Mock del cliente Supabase
- `sample_task_data`: Datos de ejemplo para una tarea
- `sample_subtask_data`: Datos de ejemplo para una subtarea
- `sample_pomodoro_data`: Datos de ejemplo para un pomodoro
- `sample_distraction_data`: Datos de ejemplo para una distracción
- `mock_supabase_response`: Helper para crear respuestas mock
- `mock_table_query`: Helper para mockear operaciones de tabla

## 📝 Escribir Nuevos Tests

### Estructura de un test

```python
def test_nombre_descriptivo(self, fixtures_necesarias):
    """Descripción del test"""
    # Arrange (preparar)
    # Act (ejecutar)
    # Assert (verificar)
```

### Ejemplo de Test Unitario

```python
@patch('app.services.task_service.get_supabase')
def test_create_task_unit(self, mock_get_supabase, sample_task_data):
    """Test unitario: crear tarea - solo prueba la lógica de insert"""
    # Arrange
    mock_supabase = MagicMock()
    mock_get_supabase.return_value = mock_supabase
    # ... configurar mocks
    
    # Act
    result = TaskService.create_task(task_create)
    
    # Assert
    assert result.title == "Test"
```

## 🔍 Tipos de Tests

### Tests Unitarios

**Los tests unitarios prueban métodos aislados**, mockeando TODAS las dependencias:

- **Archivos**: `test_*_service_unit.py`
- **Características**:
  - Cada método se prueba de forma aislada
  - Se mockean llamadas a otros métodos del mismo servicio
  - Se mockean llamadas a otros servicios
  - No dependen de la estructura de la aplicación completa

**Ejemplos:**
- `test_task_service_unit.py` - Tests unitarios para TaskService
- `test_subtask_service_unit.py` - Tests unitarios para SubtaskService
- `test_pomodoro_service_unit.py` - Tests unitarios para PomodoroService

### Tests de Integración

**Los tests de integración prueban la integración entre componentes**:

- **Archivos**: `test_integration_*.py`
- **Características**:
  - Prueban endpoints HTTP completos
  - Verifican que los servicios trabajen juntos
  - Pueden probar flujos completos de negocio

**Ejemplos:**
- `test_integration_routers.py` - Tests de integración para endpoints API

### ⚠️ Nota Importante

Los archivos `test_*_service.py` (sin `_unit`) y `test_routers.py` son tests **legacy/mixtos** que no son puramente unitarios. Para tests verdaderamente unitarios, usa los archivos `*_unit.py`.

## ⚠️ Notas Importantes

1. **Mocks de Supabase**: Todos los tests usan mocks para no necesitar una conexión real a Supabase
2. **Aislamiento**: Cada test es independiente y no depende de otros
3. **Fixtures**: Usa las fixtures proporcionadas para datos de prueba consistentes
4. **Naming**: Los nombres de tests deben ser descriptivos (`test_que_deberia_pasar`)

## 🐛 Troubleshooting

### Error: "No module named 'pytest'"

```bash
pip install -r requirements.txt
```

### Error: "ModuleNotFoundError: No module named 'app'"

Asegúrate de estar en el directorio raíz del proyecto (`backend/`) al ejecutar pytest.

### Tests fallan por mocks incorrectos

Verifica que los mocks estén configurados correctamente para simular las respuestas de Supabase.

### Cobertura baja

Ejecuta `pytest --cov=app --cov-report=term-missing` para ver qué líneas no están cubiertas y agrega tests.

## 📚 Recursos

- [Documentación de pytest](https://docs.pytest.org/)
- [Testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)
- [Unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

**¡Mantén tus tests actualizados al agregar nuevas funcionalidades!** 🎯
