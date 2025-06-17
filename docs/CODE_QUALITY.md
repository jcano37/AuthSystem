# 🐍 Code Quality Guide - Auth Backend

This project uses automated tools to maintain the quality and consistency of the Python code.

## 🛠️ Installed Tools

- **Black** - Automatic code formatting
- **isort** - Import sorting
- **flake8** - Linting and style checking
- **mypy** - Static type checking

## 📋 Available Scripts

### 1. Main Script: `format_and_check.ps1`

Complete script with all checks and advanced options.

```powershell
# Format and check all code
.\format_and_check.ps1

# Only check (do not make changes)
.\format_and_check.ps1 --check-only

# Format with detailed output
.\format_and_check.ps1 --verbose

# View full help
.\format_and_check.ps1 --help
```

### 2. Quick Script: `quick_format.ps1`

Quick formatting for daily use.

```powershell
# Quick formatting (isort + black)
.\quick_format.ps1
```

## ⚙️ Configuration

### pyproject.toml
Configuration for **black**, **isort**, and **mypy**:
- Line length: 88 characters
- Compatible with Python 3.11+
- Excludes specific directories (alembic, cache, etc.)

### setup.cfg  
Configuration for **flake8**:
- Maximum length: 88 characters
- Maximum complexity: 10
- Ignores conflicts with black

## 🚀 Recommended Usage

### During Development
```powershell
# Before each commit
.\quick_format.ps1
```

### Before Push/PR
```powershell
# Full check
.\format_and_check.ps1 --check-only
```

### In CI/CD
```powershell
# Check without changes
.\format_and_check.ps1 --check-only --verbose
```

## 📖 Manual Commands

If you prefer to run the tools individually:

```powershell
# Sort imports
python -m isort app

# Format code
python -m black app

# Check style
python -m flake8 app

# Check types
python -m mypy app
```

## 🔧 Troubleshooting

### Error: "Tool not found"
```powershell
python -m pip install black flake8 isort mypy
```

### Error: "'app' directory not found"
Run the scripts from the project root where the `app/` folder is located.

### MyPy Errors
- Review function types
- Add missing imports in `pyproject.toml`
- Use `# type: ignore` only when necessary

### Flake8 Errors
- Most are fixed by black and isort
- Manually review complexity errors
- Some may require refactoring

## 📊 Interpreting Results

- ✅ **SUCCESS**: No issues
- ❌ **FAILED**: Errors were found that require attention

### Common Error Types

1. **Black/isort**: Automatically fixed upon formatting
2. **flake8**: Style issues that require manual review
3. **mypy**: Type issues that require annotations

## 🎯 Project Standards

- **Line length**: 88 characters (black standard)
- **Imports**: Sorted by isort (stdlib → third-party → local)
- **Types**: Mandatory annotations in public functions
- **Complexity**: Maximum 10 (McCabe)

## 🔄 Git Integration

Consider adding a pre-commit hook:

```bash
# .git/hooks/pre-commit
#!/bin/sh
pwsh -File format_and_check.ps1 --check-only
```

## 💡 Tips

1. **Run formatting frequently** to avoid large changes
2. **Use --verbose** when you have hard-to-understand errors
3. **Review the configuration** in `pyproject.toml` if you need adjustments
4. **Ignore specific errors** only when absolutely necessary

---

For more information about each tool:
- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://isort.readthedocs.io/)
- [flake8 Documentation](https://flake8.pycqa.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
