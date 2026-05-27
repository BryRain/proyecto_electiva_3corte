from backend.app import app
from backend.database.models import User

with app.app_context():
    u = User.query.filter_by(email='test@test.com').first()
    if u:
        print(f'✓ Usuario existe: {u.email}')
        print(f'  Username: {u.username}')
        print(f'  Password hash: {u.password_hash[:30]}...')
        result = u.check_password('password123')
        print(f'  Password check: {result}')
    else:
        print('✗ Usuario no existe')
