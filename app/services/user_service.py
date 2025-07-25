from app import db, bcrypt
from app.models.user import User
from app.utils.validators import UserCreateSchema, UserUpdateSchema
from app.utils.exceptions import UserNotFoundError, EmailExistsError, AuthenticationError
from sqlalchemy.exc import IntegrityError
from flask import current_app

class UserService:
    @staticmethod
    def create_user(data):
        """Create a new user with validation"""
        schema = UserCreateSchema()
        validated_data = schema.load(data)
        
        # Hash password
        password_hash = bcrypt.generate_password_hash(validated_data['password']).decode('utf-8')
        
        user = User(
            name=validated_data['name'],
            email=validated_data['email'],
            password_hash=password_hash
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(f'User created: {user.email}')
            return user
        except IntegrityError:
            db.session.rollback()
            raise EmailExistsError('Email already exists')
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        if not isinstance(user_id, int) or user_id <= 0:
            raise UserNotFoundError('Invalid user ID')
            
        user = User.query.get(user_id)
        if not user:
            raise UserNotFoundError(f'User with ID {user_id} not found')
        return user
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        return User.query.all()
    
    @staticmethod
    def update_user(user_id, data):
        """Update user with validation"""
        user = UserService.get_user_by_id(user_id)
        
        schema = UserUpdateSchema()
        validated_data = schema.load(data)
        
        # Check email uniqueness if updating email
        if 'email' in validated_data:
            existing_user = User.query.filter_by(email=validated_data['email']).first()
            if existing_user and existing_user.id != user.id:
                raise EmailExistsError('Email already exists')
        
        # Update fields
        for field, value in validated_data.items():
            if field == 'password':
                user.password_hash = bcrypt.generate_password_hash(value).decode('utf-8')
            else:
                setattr(user, field, value)
        
        try:
            db.session.commit()
            current_app.logger.info(f'User updated: {user.email}')
            return user
        except IntegrityError:
            db.session.rollback()
            raise EmailExistsError('Email already exists')
    
    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        user = UserService.get_user_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        current_app.logger.info(f'User deleted: {user.email}')
        return True
    
    @staticmethod
    def search_users_by_name(name):
        """Search users by name (case-insensitive)"""
        if not name or not name.strip():
            return []
        return User.query.filter(User.name.ilike(f'%{name.strip()}%')).all()
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user credentials"""
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            current_app.logger.info(f'User authenticated: {user.email}')
            return user
        
        current_app.logger.warning(f'Authentication failed for email: {email}')
        raise AuthenticationError('Invalid email or password')
