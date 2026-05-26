from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.database.models import db, User
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar nuevo usuario"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password') or not data.get('username'):
            return jsonify({'error': 'Email, username y password son requeridos'}), 400
        
        # Validar que el usuario no exista
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'El email ya está registrado'}), 409
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'El username ya está registrado'}), 409
        
        # Crear nuevo usuario
        user = User(
            email=data['email'],
            username=data['username'],
            full_name=data.get('full_name', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email y password son requeridos'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Email o contraseña incorrectos'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Usuario inactivo'}), 401
        
        # Crear token JWT
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Sesión iniciada',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Obtener usuario actual"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify(user.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
    """Refrescar token JWT"""
    try:
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout (en producción añadir blacklist)"""
    return jsonify({'message': 'Sesión cerrada'}), 200
