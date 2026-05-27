from backend.app import app
from backend.database.models import db, User

with app.app_context():
    # Delete existing user
    user = User.query.filter_by(email='test@test.com').first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print('✓ Usuario eliminado')
    
    # Create new user
    new_user = User(
        email='admin@admin.com',
        username='admin',
        full_name='Admin User',
        is_active=True
    )
    new_user.set_password('admin123')
    
    db.session.add(new_user)
    db.session.commit()
    
    # Verify
    verify = User.query.filter_by(email='admin@admin.com').first()
    print(f'✓ Nuevo usuario creado: {verify.email}')
    print(f'  Password check: {verify.check_password("admin123")}')
