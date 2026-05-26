"""
Inicialización de Base de Datos
"""
import os
import sys

# Add parent directories to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.dirname(backend_dir))

from app import app, db
from database.models import User, Property
import bcrypt

def init_database():
    """Inicializar base de datos con datos de ejemplo"""
    
    with app.app_context():
        # Crear tablas
        db.create_all()
        print("✓ Tablas creadas")
        
        # Crear usuario de prueba
        if User.query.count() == 0:
            user = User(
                email='demo@example.com',
                username='demo',
                full_name='Usuario Demo'
            )
            user.set_password('password123')
            db.session.add(user)
            print("✓ Usuario demo creado")
        
        # Crear propiedades de ejemplo
        if Property.query.count() == 0:
            properties_data = [
                {
                    'address': 'Calle Principal 123',
                    'city': 'Medellín',
                    'state': 'Antioquia',
                    'country': 'Colombia',
                    'price': 280000,
                    'bedrooms': 3,
                    'bathrooms': 2,
                    'area_sqm': 2500,
                    'property_type': 'apartment',
                    'description': 'Apartamento moderno en zona de alto valor',
                    'amenities': ['Pool', 'Gym', 'Security'],
                    'available': True
                },
                {
                    'address': 'Carrera 50 #45-67',
                    'city': 'Bogotá',
                    'state': 'Cundinamarca',
                    'country': 'Colombia',
                    'price': 350000,
                    'bedrooms': 4,
                    'bathrooms': 3,
                    'area_sqm': 3200,
                    'property_type': 'house',
                    'description': 'Casa lujosa con jardín y garaje',
                    'amenities': ['Garden', 'Garage', 'Parking'],
                    'available': True
                },
                {
                    'address': 'Av. Paseo Peatonal 99',
                    'city': 'Cali',
                    'state': 'Valle del Cauca',
                    'country': 'Colombia',
                    'price': 200000,
                    'bedrooms': 2,
                    'bathrooms': 2,
                    'area_sqm': 1800,
                    'property_type': 'apartment',
                    'description': 'Apartamento acogedor en el centro',
                    'amenities': ['Parking'],
                    'available': True
                }
            ]
            
            for prop_data in properties_data:
                prop = Property(**prop_data)
                db.session.add(prop)
            
            print(f"✓ {len(properties_data)} propiedades de ejemplo creadas")
        
        db.session.commit()
        print("\n✓ Base de datos inicializada correctamente")

if __name__ == '__main__':
    init_database()
