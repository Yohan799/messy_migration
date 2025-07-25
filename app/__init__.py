import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    from app.routes.users import users_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    
    # Global error handlers
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({
            'error': 'Validation failed',
            'message': e.messages
        }), 400
    
    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        app.logger.error(f'Server Error: {e}')
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    # Health check endpoint
    @app.route('/')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'User Management API is running'
        })
    
    return app
