from backend.app import app
from backend.database.models import db, User

with app.app_context():
    # Check if user exists
    existing = User.query.filter_by(email='test@test.com').first()
    if existing:
        print('Usuario ya existe')
    else:
        user = User(
            email='test@test.com',
            username='testuser',
            full_name='Test User'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        print('✓ Usuario creado: test@test.com / password123')
