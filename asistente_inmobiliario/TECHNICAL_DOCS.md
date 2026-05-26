# Asistente Inmobiliario Inteligente - Documentación Técnica

## Arquitectura del Sistema 🏗️

### Capas de la Aplicación

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (HTML/JS)                       │
│  - Single Page Application (SPA)                            │
│  - Vanilla JavaScript (sin dependencias externas)           │
│  - Comunicación REST con backend                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  API GATEWAY (Flask)                         │
│  - Rutas REST                                               │
│  - Autenticación JWT                                        │
│  - CORS habilitado                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬─────────────────┐
        ▼            ▼            ▼                 ▼
┌──────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
│ Multi-Agent  │  │   RAG    │  │ Database │  │  MCP Server  │
│ System       │  │  System  │  │  (SQL)   │  │  (FastAPI)   │
│ (Claude AI)  │  │(Chroma)  │  │          │  │              │
└──────────────┘  └──────────┘  └──────────┘  └──────────────┘
```

## Componentes Principales 🧩

### 1. Sistema de Autenticación (JWT)

**Archivo:** `backend/auth/auth_routes.py`

**Flujo:**
```
Usuario Input (email, password)
    ↓
Validación de entrada
    ↓
Búsqueda en BD
    ↓
Verificación de contraseña (bcrypt)
    ↓
Generación de JWT Token
    ↓
Almacenamiento en localStorage (frontend)
```

**Token Estructura:**
```json
{
  "sub": "user_id",
  "exp": "timestamp_expiracion",
  "iat": "timestamp_creacion"
}
```

### 2. Base de Datos (SQLAlchemy)

**Archivo:** `backend/database/models.py`

**Tablas:**
- `User`: Usuarios registrados
- `Property`: Propiedades inmobiliarias
- `SearchHistory`: Historial de búsquedas
- `Document`: Documentos procesados para RAG
- `user_property_favorite`: Relación muchos-a-muchos

**Índices para optimización:**
- user.email (UNIQUE)
- user.username (UNIQUE)
- property.city, property.price (búsquedas frecuentes)
- property.available (filtros)

### 3. Sistema Multi-Agent 🤖

**Archivo:** `backend/agents/multi_agent.py`

**Arquitectura de Agentes:**

```
┌─────────────────────────────────────────────────────────┐
│              Multi-Agent Orchestrator                    │
└────────────┬────────────┬────────────┬────────────┬──────┘
             │            │            │            │
        ┌────▼──┐    ┌────▼──┐    ┌───▼────┐    ┌──▼───┐
        │Search │    │Property│   │Financial  │Legal │
        │Agent  │    │Evaluator   │Advisor   │Agent │
        └────────┘    └────────┘   └──────────┘ └─────┘
             │            │            │            │
             └────────────┼────────────┼────────────┘
                          │
                    ┌─────▼──────┐
                    │Coordinator │ (Synthesis)
                    └────────────┘
```

**Flujo de ejecución:**

1. **SearchAgent**: Analiza query, busca propiedades
2. **PropertyEvaluator**: Evalúa propiedades encontradas
3. **FinancialAdvisor**: Calcula hipotecas, affordability
4. **LegalAdvisor**: Considera aspectos legales
5. **Coordinator**: Sintetiza todas las perspectivas

**Implementación:**
- Cada agente es una instancia de Claude AI
- Se ejecutan secuencialmente (pueden ser paralelos en v2)
- Comparten contexto a través de diccionarios
- La salida de uno alimenta la entrada del siguiente

### 4. Sistema RAG (Retrieval-Augmented Generation)

**Archivos:** 
- `backend/rag/vector_store.py`
- `backend/rag/document_processor.py`

**Flujo RAG:**

```
Documento (PDF/TXT)
    ↓
Extracción de texto (PyPDF2)
    ↓
Chunking (500 caracteres, overlap 50)
    ↓
Embeddings (OpenAI)
    ↓
Almacenamiento en Chroma
    ↓
Búsqueda por similitud vectorial
```

**Búsqueda Vectorial:**

```python
# Query del usuario
query = "Apartamento en Medellín bajo $300,000"

# Generar embedding del query
query_embedding = embeddings.embed_query(query)

# Buscar documentos similares
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

# Retornar documentos + metadata + similitud
```

**Base de Datos Vectorial (Chroma):**
- Persistente en `/data/vectordb/`
- Espacio de búsqueda: COSINE
- Índice: HNSW
- Escalabilidad: millones de vectores

### 5. MCP Server

**Archivo:** `backend/mcp_server/server.py`

**Arquitectura:**
```
FastAPI Server (puerto 8001)
    │
    ├── /tools/execute (POST)
    │   └── Ejecuta herramientas según nombre
    │
    ├── /tools/list (GET)
    │   └── Lista herramientas disponibles
    │
    └── /health (GET)
        └── Estado del servidor
```

**Herramientas Disponibles:**

1. **search_web_properties**
   - Busca propiedades en web
   - Parámetros: location, price_range, property_type
   - Retorna: lista de propiedades

2. **get_market_data**
   - Datos del mercado inmobiliario
   - Parámetros: location
   - Retorna: precio promedio, tendencia, demanda

3. **get_property_details**
   - Detalles completos de una propiedad
   - Parámetros: property_id
   - Retorna: información completa

4. **search_documents**
   - Busca en sistema RAG
   - Parámetros: query
   - Retorna: documentos relevantes

## Flujo Completo de Búsqueda IA 🔄

```
1. Usuario ingresa query
   ↓
2. Frontend envía POST a /api/ai/search
   ↓
3. Backend recibe query
   ├─ Búsqueda vectorial RAG
   ├─ Búsqueda en base de datos de propiedades
   └─ Contextualización
   ↓
4. Multi-Agent Workflow
   ├─ SearchAgent: encuentra propiedades
   ├─ PropertyEvaluator: analiza valor
   ├─ FinancialAdvisor: calcula hipoteca
   ├─ LegalAdvisor: revisa legalidades
   └─ Coordinator: sintetiza todo
   ↓
5. MCP Server (opcional)
   └─ Herramientas adicionales si es necesario
   ↓
6. Compilar respuesta
   ├─ Síntesis del Coordinator
   ├─ Resultados RAG
   └─ Propiedades encontradas
   ↓
7. Guardar en historial de búsqueda
   ↓
8. Retornar respuesta al frontend
   ↓
9. Frontend renderiza resultados
```

## Seguridad 🔒

### Autenticación
- Contraseñas: Bcrypt con salt
- Tokens: JWT con expiración (24h)
- Headers: Authorization Bearer

### Protección CSRF
- Flask-CORS configurado
- Validación de origen

### Validación de Entrada
- Pydantic models en MCP
- SQLAlchemy ORM (previene SQL injection)
- Sanitización en frontend

### Base de Datos
- SQLite en desarrollo (cambiar a PostgreSQL en prod)
- Encriptación de contraseñas
- No almacenar tokens

## Performance 📊

### Optimizaciones Implementadas

1. **Base de Datos:**
   - Índices en campos frecuentes
   - Paginación (12 items por página)
   - Query lazy loading

2. **RAG:**
   - Chroma con HNSW (búsqueda O(log n))
   - Vectores cacheados
   - Búsqueda top-k

3. **Frontend:**
   - Vanilla JS (sin overhead de framework)
   - CSS crítico inline
   - Lazy loading de imágenes

4. **API:**
   - Compresión gzip
   - Cache headers
   - Respuestas JSON

## Escalabilidad 📈

### Mejoras para Producción

1. **Base de Datos:**
   ```python
   # Cambiar a PostgreSQL
   DATABASE_URL=postgresql://user:pass@host/db
   ```

2. **Caché:**
   ```python
   # Añadir Redis
   REDIS_URL=redis://localhost:6379
   ```

3. **Búsqueda:**
   ```python
   # Usar Elasticsearch o Milvus
   # para búsqueda vectorial a escala
   ```

4. **Frontend:**
   ```javascript
   // Usar CDN para assets
   // Minificar CSS/JS
   // Precomprimir GZIP
   ```

## Deployment 🚀

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend.app:app"]
```

### Environment Variables

```env
FLASK_ENV=production
SECRET_KEY=your-production-key
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://...
```

## Testing 🧪

### Unit Tests

```python
# tests/test_auth.py
def test_user_registration():
    response = client.post('/api/auth/register', {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 201

def test_user_login():
    response = client.post('/api/auth/login', {
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
```

## Troubleshooting 🔧

### Error: "No such file or directory: 'inmobiliario.db'"
```bash
cd backend
python database/init_db.py
```

### Error: "CORS error"
```python
# Verificar CORS_ORIGINS en config.py
# Añadir URL del frontend
```

### Error: "OpenAI API rate limit"
```python
# Añadir retry logic
import time
time.sleep(1)  # Rate limit: 1 req/sec
```

## Métricas y Monitoreo 📈

```python
# Ejemplo de logging
import logging

logger = logging.getLogger(__name__)
logger.info(f"Search executed for user {user_id}")
logger.warning(f"High API latency: {response_time}ms")
logger.error(f"Database connection failed: {error}")
```

## Conclusión

Este sistema integra tecnologías modernas de IA:
- ✅ Multi-Agent orchestration
- ✅ RAG (Retrieval-Augmented Generation)
- ✅ Vector search (Embeddings)
- ✅ MCP Server para extensibilidad
- ✅ Sistema de autenticación seguro
- ✅ Database relacional + vectorial
- ✅ Frontend responsivo
- ✅ API RESTful completa

Ideal para aplicaciones que requieren análisis inteligente con contexto.
