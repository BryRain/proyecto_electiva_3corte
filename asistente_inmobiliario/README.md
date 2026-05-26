# Asistente Inmobiliario Inteligente 🏠

## Descripción del Proyecto

Sistema completo de búsqueda y asesoramiento inmobiliario inteligente que utiliza **IA multi-agent**, **búsqueda vectorial (RAG)** y **MCP Server** para proporcionar recomendaciones personalizadas.

## Características Principales ✨

### 1. **Autenticación (Login/Registro)**
- Sistema JWT seguro
- Encriptación de contraseñas con bcrypt
- Recuperación de contraseña (opcional)

### 2. **Multi-Agent System (A2A)**
- **5 Agentes Especializados:**
  - 🔍 **SearchAgent**: Búsqueda y filtrado de propiedades
  - 💰 **PropertyEvaluator**: Valoración e inversión
  - 💳 **FinancialAdvisor**: Cálculos hipotecarios
  - ⚖️ **LegalAdvisor**: Asesoramiento legal
  - 📋 **Coordinator**: Síntesis de recomendaciones

### 3. **Sistema RAG (Retrieval-Augmented Generation)**
- Procesa PDFs y documentos
- Búsqueda vectorial con Chroma
- Embeddings OpenAI

### 4. **Búsqueda Vectorial**
- Búsqueda por similitud en documentos
- Base de datos vectorial persistente
- Relevancia calculada

### 5. **Flujo de IA Integrado**
- Búsqueda inteligente con contexto
- Análisis multi-perspectiva
- Síntesis automática de recomendaciones

### 6. **MCP Server (Optional + Note Boost)**
- FastAPI backend para herramientas
- Búsqueda web de propiedades
- Análisis de mercado
- Información de documentos

## Estructura del Proyecto 📂

```
asistente_inmobiliario/
├── backend/
│   ├── app.py                      # Aplicación Flask principal
│   ├── config.py                   # Configuración
│   ├── requirements.txt            # Dependencias
│   │
│   ├── auth/
│   │   └── auth_routes.py         # Rutas de autenticación JWT
│   │
│   ├── database/
│   │   ├── models.py              # SQLAlchemy models
│   │   └── init_db.py             # Inicialización BD
│   │
│   ├── agents/
│   │   └── multi_agent.py         # Sistema Multi-Agent
│   │
│   ├── rag/
│   │   ├── vector_store.py        # Chroma Vector Store
│   │   └── document_processor.py  # Procesamiento PDFs
│   │
│   └── mcp_server/
│       └── server.py              # MCP FastAPI Server
│
├── frontend/
│   ├── index.html                 # Interfaz principal
│   ├── css/style.css              # Estilos responsive
│   ├── js/
│   │   ├── api.js                 # Cliente HTTP
│   │   ├── auth.js                # Autenticación
│   │   ├── ui.js                  # Componentes UI
│   │   └── app.js                 # Lógica principal
│   └── assets/                    # Imágenes e iconos
│
├── documents/                     # PDFs para RAG
├── data/
│   └── vectordb/                  # Base de datos vectorial
│
├── .env.example                   # Variables de entorno
└── README.md                      # Este archivo

```

## Requisitos 📋

- Python 3.8+
- Node.js (opcional, para frontend mejorado)
- API Key de OpenAI o Anthropic
- SQLite (incluido en Python)

## Instalación 🚀

### 1. Clonar/Descargar el proyecto
```bash
cd asistente_inmobiliario
```

### 2. Crear entorno virtual Python
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r backend/requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus API keys
```

### 5. Inicializar base de datos
```bash
cd backend
python database/init_db.py
```

### 6. Ejecutar el servidor
```bash
python app.py
```

El servidor estará disponible en: **http://localhost:5000**

## Uso 💻

### Login/Registro
1. Ir a http://localhost:5000
2. Registro: crear nueva cuenta
3. Login: usar email y contraseña

**Credenciales de prueba:**
- Email: `demo@example.com`
- Contraseña: `password123`

### Búsqueda Inteligente con IA
```
"Busco apartamento de 3 habitaciones en Medellín, presupuesto máximo $300,000, 
con piscina y seguridad. ¿Cuál sería una buena inversión?"
```

El sistema:
1. Busca propiedades coincidentes
2. Consulta documentos RAG
3. Los 5 agentes analizan desde sus perspectivas
4. Proporciona síntesis final

### Subir Documentos (RAG)
1. Ir a pestaña "Documentos"
2. Drag & drop PDFs o TXT
3. Sistema procesa y indexa automáticamente
4. Disponible para búsquedas

### Consultar Agentes Específicos
1. Seleccionar agente
2. Escribir tarea
3. Obtener análisis especializado

## API Endpoints 🔌

### Autenticación
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
POST   /api/auth/refresh
```

### Propiedades
```
GET    /api/properties?city=&min_price=&max_price=
GET    /api/properties/<id>
POST   /api/properties
```

### Búsqueda IA
```
POST   /api/ai/search         # Búsqueda multi-agent
GET    /api/ai/agents         # Listar agentes
POST   /api/ai/agent/<name>   # Ejecutar agente específico
```

### RAG y Documentos
```
POST   /api/rag/search
POST   /api/documents/upload
POST   /api/documents/process
```

### Favoritos
```
GET    /api/favorites
POST   /api/favorites/<id>
DELETE /api/favorites/<id>
```

## MCP Server 🤖

Ejecutar MCP Server en puerto 8001:
```bash
cd backend/mcp_server
python -m uvicorn server:app --host 127.0.0.1 --port 8001
```

**Herramientas disponibles:**
- `search_web_properties`: Buscar propiedades en web
- `get_market_data`: Datos del mercado
- `get_property_details`: Detalles de propiedad
- `search_documents`: Buscar en RAG

## Flujo de IA Explicado 🧠

```
Usuario Query
    ↓
[SearchAgent] → Búsqueda de propiedades
    ↓
[PropertyEvaluator] → Análisis de valor
    ↓
[FinancialAdvisor] → Análisis hipotecario
    ↓
[LegalAdvisor] → Consideraciones legales
    ↓
[Coordinator] → Síntesis final
    ↓
Respuesta integrada al usuario
```

## Tecnologías Utilizadas 🛠️

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para bases de datos
- **Flask-JWT-Extended** - Autenticación JWT
- **Anthropic Claude** - Agentes IA
- **OpenAI** - Embeddings vectoriales
- **Chroma** - Base de datos vectorial
- **FastAPI** - MCP Server
- **PyPDF2** - Procesamiento de PDFs

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos responsive
- **JavaScript Vanilla** - Sin dependencias
- **Fetch API** - Comunicación HTTP

### Base de Datos
- **SQLite** - Desarrollo
- **PostgreSQL** - Producción (opcional)

## Variables de Entorno 🔐

```env
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta
JWT_SECRET_KEY=tu-jwt-secreto

# APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=sqlite:///inmobiliario.db
```

## Extensiones Futuras 🚀

- [ ] Mobile app (React Native)
- [ ] Video tours de propiedades
- [ ] Integración con APIs de propiedades reales
- [ ] Sistema de notificaciones
- [ ] Chat en tiempo real
- [ ] Análisis de mercado histórico
- [ ] Recomendaciones por ML
- [ ] Sistema de reviews

## Notas Importantes ⚠️

1. **Llaves API**: Reemplazar con tus propias llaves en producción
2. **Base de datos**: En producción usar PostgreSQL
3. **CORS**: Configurado para localhost, ajustar en producción
4. **Seguridad**: Cambiar SECRET_KEY en producción
5. **Velocidad**: RAG mejora con más documentos

## Troubleshooting 🔧

### Error: "OpenAI API key not found"
```bash
# Verificar .env
cat .env | grep OPENAI_API_KEY
```

### Error: "Database locked"
```bash
rm *.db  # Eliminar BD y reiniciar
python backend/database/init_db.py
```

### Frontend no conecta con backend
```javascript
// Verificar api.js
console.log(apiClient.baseURL);
```

## Contacto y Soporte 📧

Para preguntas o issues, consultar documentación en:
- [OpenAI Docs](https://platform.openai.com/docs)
- [Anthropic Docs](https://docs.anthropic.com)
- [Chroma Docs](https://docs.trychroma.com)

---

**Proyecto Final - Electiva 3 Corte** 
**Sistema Inmobiliario con IA Multi-Agent, RAG y MCP** 🏠✨
