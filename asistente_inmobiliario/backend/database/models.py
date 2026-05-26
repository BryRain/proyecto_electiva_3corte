from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    """Modelo de usuario con autenticación"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con favoritos
    favorites = db.relationship('Property', secondary='user_property_favorite', backref='favorited_by')
    
    def set_password(self, password):
        """Hashear y establecer contraseña"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verificar contraseña"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat()
        }

class Property(db.Model):
    """Modelo de propiedad inmobiliaria"""
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False, index=True)
    city = db.Column(db.String(100), nullable=False, index=True)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), default='Colombia')
    price = db.Column(db.Float, nullable=False, index=True)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    area_sqm = db.Column(db.Float)
    property_type = db.Column(db.String(50))  # apartment, house, office, etc
    description = db.Column(db.Text)
    amenities = db.Column(db.JSON)  # pool, gym, parking, etc
    images = db.Column(db.JSON)  # Lista de URLs
    available = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'price': self.price,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'area_sqm': self.area_sqm,
            'property_type': self.property_type,
            'description': self.description,
            'amenities': self.amenities,
            'images': self.images,
            'available': self.available
        }

class SearchHistory(db.Model):
    """Historial de búsquedas de usuarios"""
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    query = db.Column(db.String(500), nullable=False)
    results_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    user = db.relationship('User', backref='search_history')

class Document(db.Model):
    """Documentos procesados para RAG"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text)
    content_hash = db.Column(db.String(64), unique=True)  # SHA256
    processed = db.Column(db.Boolean, default=False)
    chunks_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Tabla de asociación muchos-a-muchos para favoritos
user_property_favorite = db.Table('user_property_favorite',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id'), primary_key=True)
)
