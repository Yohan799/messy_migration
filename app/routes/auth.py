from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.utils.validators import UserLoginSchema
from app.utils.exceptions import AuthenticationError
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        schema = UserLoginSchema()
        validated_data = schema.load(data)
        
        user = UserService.authenticate_user(
            validated_data['email'], 
            validated_data['password']
        )
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'status': 'success',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'message': e.messages}), 400
    except AuthenticationError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile (protected route example)"""
    try:
        current_user_id = get_jwt_identity()
        user = UserService.get_user_by_id(current_user_id)
        return jsonify(user.to_dict()), 200
    except UserNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve profile'}), 500
