@echo off
REM Script para ejecutar el sistema completo en Windows

echo ==================================================
echo Asistente Inmobiliario Inteligente
echo ==================================================

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias...
pip install -r backend\requirements.txt

REM Inicializar base de datos
echo Inicializando base de datos...
cd backend
python database\init_db.py
cd ..

REM Crear .env si no existe
if not exist ".env" (
    echo Creando archivo .env...
    copy .env.example .env
    echo Por favor edita .env con tus claves API
    pause
)

REM Ejecutar servidor
echo Iniciando servidor en http://localhost:5000
python backend\app.py

REM Pausar para ver mensajes de error
pause
