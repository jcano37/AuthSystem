# Workflows de GitHub Actions

## Code Quality Check

Este workflow se ejecuta automáticamente cuando se hace push o pull request a las ramas `develop`, `qa` o `main`.

### Herramientas incluidas:

1. **isort** - Ordenamiento de imports
2. **Black** - Formateo de código
3. **flake8** - Linting y verificación de estilo
4. **mypy** - Verificación de tipos
5. **format_and_check.ps1** - Script personalizado de verificación

### ¿Qué hace cada herramienta?

- **isort**: Ordena y organiza las importaciones de Python
- **Black**: Formatea el código siguiendo un estilo consistente
- **flake8**: Verifica el código contra las reglas de PEP8 y detecta errores comunes
- **mypy**: Verifica tipos estáticos para detectar errores de tipo
- **format_and_check.ps1**: Ejecuta todas las herramientas en modo verificación

### Ejecutar localmente

Para ejecutar las mismas verificaciones localmente:

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar el script completo
./format_and_check.ps1 --check-only --verbose

# O ejecutar herramientas individualmente:
python -m isort --check-only --diff app
python -m black --check --diff app
python -m flake8 app
python -m mypy app
```

### Configuración

Las configuraciones están en:
- `pyproject.toml` - Black, isort, mypy
- `setup.cfg` - flake8 