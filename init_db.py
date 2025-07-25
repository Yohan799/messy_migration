from app import create_app, db
from app.models.user import User

def init_database():
    """Initialize the database with tables"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if admin user exists, if not create one
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            from app import bcrypt
            admin = User(
                name='Admin User',
                email='admin@example.com',
                password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8')
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin@example.com / admin123")

if __name__ == '__main__':
    init_database()