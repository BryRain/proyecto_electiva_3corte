from backend.app import app
from backend.database.models import User

with app.app_context():
    u = User.query.filter_by(email='test@test.com').first()
    if u:
        print(f'✓ Usuario: {u.email}')
        print(f'  is_active: {u.is_active}')
        if not u.is_active:
            print('  → Activando usuario...')
            u.is_active = True
            from backend.database.models import db
            db.session.commit()
            print('  ✓ Usuario activado')
    else:
        print('✗ Usuario no existe')
