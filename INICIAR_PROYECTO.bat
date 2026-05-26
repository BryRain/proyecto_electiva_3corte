@echo off
REM Script de inicio rápido para Windows
REM Asistente Inmobiliario IA

cls
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║            ASISTENTE INMOBILIARIO INTELIGENTE CON IA              ║
echo ║                   Script de Inicio - Windows                      ║
echo ║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

REM Cambiar a directorio del proyecto
cd /d "C:\Users\Bryan\Documents\proyecto_electiva_3Corte\asistente_inmobiliario"

echo [1/4] Verificando entorno virtual...
if exist "venv\Scripts\activate.bat" (
    echo ✓ Entorno virtual encontrado
) else (
    echo ✗ Creando entorno virtual...
    python -m venv venv
    echo ✓ Entorno virtual creado
)

echo.
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat
echo ✓ Entorno virtual activado

echo.
echo [3/4] Verificando dependencias...
pip install -q -r backend\requirements.txt >nul 2>&1
echo ✓ Dependencias instaladas

echo.
echo [4/4] Inicializando base de datos...
cd backend
python database\init_db.py >nul 2>&1
cd ..
echo ✓ Base de datos inicializada

echo.
echo ════════════════════════════════════════════════════════════════════
echo ✨ LISTO PARA EJECUTAR
echo ════════════════════════════════════════════════════════════════════
echo.
echo 🔐 Credenciales de Prueba:
echo    Email:    demo@example.com
echo    Password: password123
echo.
echo 📝 IMPORTANTE: Asegúrate de que .env tenga tus API keys:
echo    - OPENAI_API_KEY
echo    - ANTHROPIC_API_KEY
echo.
echo 🚀 Iniciando servidor en http://localhost:5000 ...
echo.
echo (Presiona CTRL+C para detener)
echo.

REM Ejecutar la aplicación
python backend\app.py

pause
