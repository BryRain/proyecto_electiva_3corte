"""
Script para poblar la base de datos con propiedades colombianas
"""
import os
import sys

from backend.database.models import db, Property
from backend.app import app
import random

# Datos de ciudades colombianas con sus departamentos
CIUDADES_COLOMBIA = {
    'Bogotá': 'Cundinamarca',
    'Medellín': 'Antioquia',
    'Cali': 'Valle del Cauca',
    'Barranquilla': 'Atlántico',
    'Cartagena': 'Bolívar',
    'Cúcuta': 'Norte de Santander',
    'Bucaramanga': 'Santander',
    'Santa Marta': 'Magdalena',
    'Manizales': 'Caldas',
    'Pereira': 'Risaralda',
    'Armenia': 'Quindío',
    'Ibagué': 'Tolima',
    'Neiva': 'Huila',
    'Popayán': 'Cauca',
    'Pasto': 'Nariño',
}

TIPOS_PROPIEDAD = ['apartment', 'house']
AMENIDADES = [
    ['Piscina', 'Gimnasio', 'Parqueadero'],
    ['Parqueadero', 'Seguridad 24h'],
    ['Piscina', 'Área verde', 'Parqueadero'],
    ['Gimnasio', 'Zona común'],
    ['Seguridad 24h', 'Parqueadero'],
]

def generar_propiedades():
    """Generar lista de propiedades para poblar la BD"""
    propiedades = []
    
    for ciudad, departamento in CIUDADES_COLOMBIA.items():
        num_propiedades = random.randint(8, 15)
        
        for i in range(num_propiedades):
            tipo_propiedad = random.choice(TIPOS_PROPIEDAD)
            es_arriendo = random.choice([True, False])
            
            if es_arriendo:
                if tipo_propiedad == 'apartment':
                    precio = random.randint(800000, 3000000)
                else:
                    precio = random.randint(1000000, 4000000)
            else:
                if tipo_propiedad == 'apartment':
                    precio = random.randint(150000000, 800000000)
                else:
                    precio = random.randint(300000000, 1500000000)
            
            bedrooms = random.randint(1, 5)
            bathrooms = random.randint(1, 3)
            area = random.randint(50, 300)
            
            propiedad = {
                'address': f"Calle {random.randint(1, 150)} #{random.randint(1, 100)}-{random.randint(1, 99)}, {ciudad}",
                'city': ciudad,
                'state': departamento,
                'country': 'Colombia',
                'price': precio,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area_sqm': area,
                'property_type': tipo_propiedad,
                'description': f"Excelente {tipo_propiedad} en {ciudad}",
                'amenities': random.choice(AMENIDADES),
                'available': True,
                'images': []
            }
            propiedades.append(propiedad)
    
    return propiedades

if __name__ == '__main__':
    with app.app_context():
        count = Property.query.count()
        
        if count > 0:
            print(f"✓ Base de datos ya contiene {count} propiedades.")
            sys.exit(0)
        
        print("Generando propiedades colombianas...")
        propiedades = generar_propiedades()
        
        print(f"Insertando {len(propiedades)} propiedades...")
        
        for prop in propiedades:
            property_obj = Property(**prop)
            db.session.add(property_obj)
        
        db.session.commit()
        print(f"✓ {len(propiedades)} propiedades insertadas!")
