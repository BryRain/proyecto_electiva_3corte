from backend.app import app
from backend.database.models import db

"""
Script de utilidades para administración del proyecto
"""

def reset_database():
    """Resetear base de datos"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✓ Base de datos reseteada")

def seed_sample_data():
    """Llenar con datos de ejemplo"""
    from backend.database.models import User, Property
    
    with app.app_context():
        # Crear usuario
        user = User(
            email='test@example.com',
            username='testuser',
            full_name='Test User'
        )
        user.set_password('test123')
        db.session.add(user)
        
        # Crear propiedades
        for i in range(10):
            prop = Property(
                address=f'Dirección de Ejemplo {i+1}',
                city=['Medellín', 'Bogotá', 'Cali'][i % 3],
                state='Departamento',
                country='Colombia',
                price=200000 + (i * 50000),
                bedrooms=2 + (i % 3),
                bathrooms=1 + (i % 2),
                area_sqm=1500 + (i * 100),
                property_type=['apartment', 'house', 'office'][i % 3],
                description=f'Propiedad de ejemplo {i+1}',
                available=True
            )
            db.session.add(prop)
        
        db.session.commit()
        print(f"✓ Datos de ejemplo cargados")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'reset':
            reset_database()
        elif sys.argv[1] == 'seed':
            seed_sample_data()
    else:
        print("""
        Utilidades disponibles:
        python utils.py reset    - Resetear base de datos
        python utils.py seed     - Cargar datos de ejemplo
        """)
