# Script para ejecutar todo el proyecto

Write-Host "=== ASISTENTE INMOBILIARIO - Setup Completo ===" -ForegroundColor Green

# Activar venv
Write-Host "`n1. Activando entorno virtual..." -ForegroundColor Cyan
& "C:\Users\Bryan\Documents\proyecto_electiva_3Corte\venv\Scripts\Activate.ps1"

# Crear tablas
Write-Host "`n2. Creando tablas en la base de datos..." -ForegroundColor Cyan
python << 'PYTHON'
from backend.app import app
from backend.database.models import db

with app.app_context():
    db.create_all()
    print("✓ Tablas creadas exitosamente")
PYTHON

# Poblar BD
Write-Host "`n3. Poblando base de datos con propiedades..." -ForegroundColor Cyan
python -m backend.database.populate_db

# Iniciar backend
Write-Host "`n4. Iniciando servidor backend..." -ForegroundColor Cyan
Write-Host "   → Accede a http://localhost:5000" -ForegroundColor Yellow
Write-Host "   → Presiona CTRL+C para detener" -ForegroundColor Yellow

python -m backend.app
