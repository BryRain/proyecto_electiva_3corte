#!/bin/bash
# Script para ejecutar el sistema completo en Linux/Mac

echo "=================================================="
echo "Asistente Inmobiliario Inteligente"
echo "=================================================="

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r backend/requirements.txt

# Inicializar base de datos
echo "Inicializando base de datos..."
cd backend
python database/init_db.py
cd ..

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo "Creando archivo .env..."
    cp .env.example .env
    echo "Por favor edita .env con tus claves API"
fi

# Ejecutar servidor
echo "Iniciando servidor en http://localhost:5000"
python backend/app.py
