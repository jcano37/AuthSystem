# 🐍 Guía de Calidad de Código - Auth Backend

Este proyecto utiliza herramientas automatizadas para mantener la calidad y consistencia del código Python.

## 🛠️ Herramientas Instaladas

- **Black** - Formateo automático de código
- **isort** - Ordenamiento de imports
- **flake8** - Linting y verificación de estilo
- **mypy** - Verificación de tipos estáticos

## 📋 Scripts Disponibles

### 1. Script Principal: `format_and_check.ps1`

Script completo con todas las verificaciones y opciones avanzadas.

```powershell
# Formatear y verificar todo el código
.\format_and_check.ps1

# Solo verificar (no hacer cambios)
.\format_and_check.ps1 --check-only

# Formatear con salida detallada
.\format_and_check.ps1 --verbose

# Ver ayuda completa
.\format_and_check.ps1 --help
```

### 2. Script Rápido: `quick_format.ps1`

Formateo rápido para uso diario.

```powershell
# Formateo rápido (isort + black)
.\quick_format.ps1
```

## ⚙️ Configuración

### pyproject.toml
Configuración para **black**, **isort** y **mypy**:
- Longitud de línea: 88 caracteres
- Compatible con Python 3.11+
- Excluye directorios específicos (alembic, cache, etc.)

### setup.cfg  
Configuración para **flake8**:
- Longitud máxima: 88 caracteres
- Complejidad máxima: 10
- Ignora conflictos con black

## 🚀 Uso Recomendado

### Durante el Desarrollo
```powershell
# Antes de cada commit
.\quick_format.ps1
```

### Antes de Push/PR
```powershell
# Verificación completa
.\format_and_check.ps1 --check-only
```

### En CI/CD
```powershell
# Verificación sin cambios
.\format_and_check.ps1 --check-only --verbose
```

## 📖 Comandos Manuales

Si prefieres ejecutar las herramientas individualmente:

```powershell
# Ordenar imports
python -m isort app

# Formatear código  
python -m black app

# Verificar estilo
python -m flake8 app

# Verificar tipos
python -m mypy app
```

## 🔧 Solución de Problemas

### Error: "Herramienta no encontrada"
```powershell
python -m pip install black flake8 isort mypy
```

### Error: "No se encontró directorio 'app'"
Ejecuta los scripts desde la raíz del proyecto donde está la carpeta `app/`.

### Errores de mypy
- Revisa los tipos de las funciones
- Agrega imports missing en `pyproject.toml`
- Usa `# type: ignore` solo cuando sea necesario

### Errores de flake8
- La mayoría se solucionan con black e isort
- Revisa manualmente errores de complejidad
- Algunos pueden requerir refactoring

## 📊 Interpretación de Resultados

- ✅ **ÉXITO**: No hay problemas
- ❌ **FALLÓ**: Se encontraron errores que requieren atención

### Tipos de Errores Comunes

1. **Black/isort**: Se solucionan automáticamente al formatear
2. **flake8**: Problemas de estilo que requieren revisión manual
3. **mypy**: Problemas de tipos que requieren anotaciones

## 🎯 Estándares del Proyecto

- **Longitud de línea**: 88 caracteres (estándar black)
- **Imports**: Ordenados por isort (stdlib → terceros → locales)
- **Tipos**: Anotaciones obligatorias en funciones públicas
- **Complejidad**: Máximo 10 (McCabe)

## 🔄 Integración con Git

Considera agregar un pre-commit hook:

```bash
# .git/hooks/pre-commit
#!/bin/sh
pwsh -File format_and_check.ps1 --check-only
```

## 💡 Tips

1. **Ejecuta formateo frecuentemente** para evitar grandes cambios
2. **Usa --verbose** cuando tengas errores difíciles de entender  
3. **Revisa la configuración** en pyproject.toml si necesitas ajustes
4. **Ignora errores específicos** solo cuando sea absolutamente necesario

---

Para más información sobre cada herramienta:
- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://isort.readthedocs.io/)
- [flake8 Documentation](https://flake8.pycqa.org/)
- [mypy Documentation](https://mypy.readthedocs.io/) 