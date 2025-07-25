import pytest
import json
from app.models.user import User

class TestUserAPI:
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_create_user_valid_data(self, client):
        """Test creating user with valid data"""
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'securepass123'
        }
        response = client.post('/users', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'John Doe'
        assert data['email'] == 'john@example.com'
        assert 'password' not in data  # Password should not be returned
    
    def test_create_user_invalid_email(self, client):
        """Test creating user with invalid email"""
        user_data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'password': 'securepass123'
        }
        response = client.post('/users',
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Validation failed' in data['error']
    
    def test_create_user_short_password(self, client):
        """Test creating user with short password"""
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': '123'  # Too short
        }
        response = client.post('/users',
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_get_user_exists(self, client, sample_user):
        """Test getting existing user"""
        response = client.get(f'/user/{sample_user.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['email'] == 'test@example.com'
    
    def test_get_user_not_exists(self, client):
        """Test getting non-existent user"""
        response = client.get('/user/999')
        assert response.status_code == 404
    
    def test_login_valid_credentials(self, client, sample_user):
        """Test login with valid credentials"""
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = client.post('/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'access_token' in data
    
    def test_login_invalid_credentials(self, client, sample_user):
        """Test login with invalid credentials"""
        login_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = client.post('/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 401
    
    def test_search_users(self, client, sample_user):
        """Test user search functionality"""
        response = client.get('/search?name=Test')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['name'] == 'Test User'
    
    def test_search_users_no_query(self, client):
        """Test user search without query parameter"""
        response = client.get('/search')
        assert response.status_code == 400