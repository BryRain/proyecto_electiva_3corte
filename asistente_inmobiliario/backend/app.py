
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from sqlalchemy import event, func
from sqlalchemy.engine import Engine
import unicodedata
import os
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

# Importar configuración
from backend.config import config, Config
from backend.database.models import db, Property, SearchHistory
from backend.auth.auth_routes import auth_bp
from backend.rag.vector_store import VectorStore
from backend.rag.document_processor import DocumentProcessor
from backend.agents.multi_agent import MultiAgent

def _normalize(text):
    if text is None:
        return None
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('ascii').lower()

@event.listens_for(Engine, "connect")
def _register_sqlite_functions(dbapi_conn, _):
    dbapi_conn.create_function("normalize_text", 1, _normalize)

# Crear aplicación Flask con carpeta estática del frontend
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app = Flask(__name__, static_folder=frontend_path, static_url_path='')
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config.get(env, Config))

# Inicializar extensiones
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Registrar blueprints de autenticación
app.register_blueprint(auth_bp)

# Inicializar componentes IA
vector_store = None
multi_agent = MultiAgent()

@app.before_request
def initialize_components():
    """Inicializar componentes en primer request"""
    global vector_store
    if vector_store is None:
        vector_store = VectorStore(app.config['RAG_DB_PATH'])

# ==================== RUTAS DE PROPIEDADES ====================

@app.route('/')
def index():
    """Servir el frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/properties', methods=['GET'])
def get_properties():
    """Obtener propiedades con filtros"""
    try:
        # Parámetros de filtro
        city = request.args.get('city')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        bedrooms = request.args.get('bedrooms', type=int)
        property_type = request.args.get('type')
        available_only = request.args.get('available', 'true').lower() == 'true'
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Construir query
        query = Property.query
        
        if city:
            query = query.filter(func.normalize_text(Property.city) == _normalize(city))
        if min_price:
            query = query.filter(Property.price >= min_price)
        if max_price:
            query = query.filter(Property.price <= max_price)
        if bedrooms:
            query = query.filter_by(bedrooms=bedrooms)
        if property_type:
            query = query.filter_by(property_type=property_type)
        if available_only:
            query = query.filter_by(available=True)
        
        # Paginar
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'properties': [p.to_dict() for p in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    """Obtener detalles de una propiedad"""
    try:
        property = Property.query.get(property_id)
        
        if not property:
            return jsonify({'error': 'Propiedad no encontrada'}), 404
        
        return jsonify(property.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/properties', methods=['POST'])
@jwt_required()
def create_property():
    """Crear nueva propiedad (admin)"""
    try:
        data = request.get_json()
        
        property = Property(
            address=data['address'],
            city=data['city'],
            state=data.get('state'),
            country=data.get('country', 'Colombia'),
            price=data['price'],
            bedrooms=data.get('bedrooms'),
            bathrooms=data.get('bathrooms'),
            area_sqm=data.get('area_sqm'),
            property_type=data.get('property_type'),
            description=data.get('description'),
            amenities=data.get('amenities'),
            images=data.get('images')
        )
        
        db.session.add(property)
        db.session.commit()
        
        return jsonify({'message': 'Propiedad creada', 'property': property.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== RUTAS DE IA Y RAG ====================

@app.route('/api/ai/search', methods=['POST'])
@jwt_required()
def ai_search():
    """Búsqueda inteligente con IA"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query es requerida'}), 400
        
        # Buscar en documentos (RAG)
        rag_results = vector_store.search(query, top_k=5)
        
        # Obtener contexto de propiedades
        properties = Property.query.filter(
            Property.description.contains(query.split()[0]) if query.split() else True
        ).limit(5).all()
        
        # Ejecutar flujo multi-agent
        ai_result = multi_agent.execute_workflow(
            user_query=query,
            user_context={
                'rag_results': rag_results,
                'properties': [p.to_dict() for p in properties],
                'user_id': user_id
            }
        )
        
        # Guardar en historial de búsqueda
        search = SearchHistory(
            user_id=user_id,
            query=query,
            results_count=len(rag_results) + len(properties)
        )
        db.session.add(search)
        db.session.commit()
        
        return jsonify({
            'query': query,
            'ai_response': ai_result,
            'rag_documents': rag_results,
            'properties_found': len(properties)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/agents', methods=['GET'])
def get_agents():
    """Obtener información de agentes disponibles"""
    try:
        agents = multi_agent.get_agents_info()
        return jsonify({
            'agents': agents,
            'total': len(agents)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/agent/<agent_name>', methods=['POST'])
@jwt_required()
def execute_agent(agent_name):
    """Ejecutar un agente específico"""
    try:
        data = request.get_json()
        task = data.get('task')
        context = data.get('context')
        
        if not task:
            return jsonify({'error': 'Task es requerida'}), 400
        
        result = multi_agent.execute_agent(agent_name, task, context)
        
        return jsonify({
            'agent': agent_name,
            'result': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RUTAS DE DOCUMENTOS ====================

@app.route('/api/documents/process', methods=['POST'])
@jwt_required()
def process_documents():
    """Procesar documentos del directorio"""
    try:
        documents_dir = app.config['DOCUMENTS_PATH']
        stats = DocumentProcessor.process_documents_from_directory(
            documents_dir,
            vector_store
        )
        
        return jsonify({
            'message': 'Documentos procesados',
            'statistics': stats
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents/upload', methods=['POST'])
@jwt_required()
def upload_document():
    """Subir documento"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if not file.filename.endswith(('.pdf', '.txt')):
            return jsonify({'error': 'Solo se aceptan PDF y TXT'}), 400
        
        # Guardar archivo
        documents_dir = app.config['DOCUMENTS_PATH']
        os.makedirs(documents_dir, exist_ok=True)
        file_path = os.path.join(documents_dir, file.filename)
        file.save(file_path)
        
        # Procesar documento
        if DocumentProcessor.process_document(file_path, vector_store):
            return jsonify({'message': 'Documento procesado exitosamente'}), 200
        else:
            return jsonify({'error': 'Error procesando documento'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RUTAS DE BÚSQUEDA VECTORIAL ====================

@app.route('/api/rag/search', methods=['POST'])
def rag_search():
    """Búsqueda vectorial en documentos"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        top_k = data.get('top_k', 5)
        
        if not query:
            return jsonify({'error': 'Query es requerida'}), 400
        
        results = vector_store.search(query, top_k=top_k)
        
        return jsonify({
            'query': query,
            'results': results,
            'total': len(results)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RUTAS DE FAVORITOS ====================

@app.route('/api/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    try:
        user_id = int(get_jwt_identity())
        from backend.database.models import User

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        favorites = [p.to_dict() for p in user.favorites]
        
        return jsonify({
            'favorites': favorites,
            'total': len(favorites)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/favorites/<int:property_id>', methods=['POST'])
@jwt_required()
def add_favorite(property_id):
    try:
        user_id = int(get_jwt_identity())
        from backend.database.models import User

        user = User.query.get(user_id)
        property = Property.query.get(property_id)
        
        if not user or not property:
            return jsonify({'error': 'Usuario o propiedad no encontrada'}), 404
        
        user.favorites.append(property)
        db.session.commit()
        
        return jsonify({'message': 'Añadido a favoritos'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/favorites/<int:property_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(property_id):
    try:
        user_id = int(get_jwt_identity())
        from backend.database.models import User

        user = User.query.get(user_id)
        property = Property.query.get(property_id)
        
        if not user or not property:
            return jsonify({'error': 'Usuario o propiedad no encontrada'}), 404
        
        if property in user.favorites:
            user.favorites.remove(property)
            db.session.commit()
        
        return jsonify({'message': 'Removido de favoritos'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Real Estate AI Assistant'
    }), 200

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Error interno del servidor'}), 500

# ==================== INICIALIZACIÓN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Crear directorio de documentos
        os.makedirs(app.config['DOCUMENTS_PATH'], exist_ok=True)
    
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5001)),
        debug=app.config['DEBUG']
    )
