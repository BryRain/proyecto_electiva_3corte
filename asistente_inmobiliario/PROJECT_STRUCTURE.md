backend/
├── __init__.py
├── app.py                      # Aplicación principal Flask
├── config.py                   # Configuración
├── requirements.txt            # Dependencias Python
│
├── auth/
│   ├── __init__.py
│   └── auth_routes.py         # Rutas de autenticación
│
├── database/
│   ├── __init__.py
│   ├── models.py              # Modelos SQLAlchemy
│   └── init_db.py             # Inicialización de BD
│
├── agents/
│   ├── __init__.py
│   └── multi_agent.py         # Sistema Multi-Agent
│
├── rag/
│   ├── __init__.py
│   ├── vector_store.py        # Vector Store con Chroma
│   └── document_processor.py  # Procesamiento de PDFs
│
└── mcp_server/
    ├── __init__.py
    └── server.py              # Servidor MCP FastAPI

frontend/
├── index.html                 # Página principal
├── css/
│   └── style.css             # Estilos
├── js/
│   ├── app.js                # Aplicación principal
│   ├── auth.js               # Autenticación
│   ├── api.js                # Cliente API
│   └── ui.js                 # Funciones UI
└── assets/
    └── (imágenes, iconos)

documents/
└── (PDFs para RAG)

data/
└── vectordb/
    └── (Base de datos vectorial Chroma)
