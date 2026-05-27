from backend.app import app
from backend.database.models import User

with app.app_context():
    user = User.query.filter_by(email='demo@demo.com').first()
    if user:
        print(f'✓ Usuario: {user.email}')
        print(f'  Username: {user.username}')
        print(f'  is_active: {user.is_active}')
        pwd_check = user.check_password('demo1234')
        print(f'  check_password("demo1234"): {pwd_check}')
    else:
        print('✗ Usuario no encontrado')
