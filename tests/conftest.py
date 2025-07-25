import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def sample_user(app):
    """Create a sample user for testing"""
    from app import bcrypt
    user = User(
        name='Test User',
        email='test@example.com',
        password_hash=bcrypt.generate_password_hash('testpass123').decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()
    return user
