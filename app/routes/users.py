from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.utils.exceptions import UserNotFoundError, EmailExistsError
from marshmallow import ValidationError

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = UserService.get_all_users()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve users'}), 500

@users_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user"""
    try:
        user = UserService.get_user_by_id(user_id)
        return jsonify(user.to_dict()), 200
    except UserNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve user'}), 500

@users_bp.route('/users', methods=['POST'])
def create_user():
    """Create new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user = UserService.create_user(data)
        return jsonify(user.to_dict()), 201
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'message': e.messages}), 400
    except EmailExistsError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': 'Failed to create user'}), 500

@users_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user = UserService.update_user(user_id, data)
        return jsonify(user.to_dict()), 200
    except UserNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'message': e.messages}), 400
    except EmailExistsError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': 'Failed to update user'}), 500

@users_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    try:
        UserService.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
    except UserNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to delete user'}), 500

@users_bp.route('/search', methods=['GET'])
def search_users():
    """Search users by name"""
    try:
        name = request.args.get('name', '').strip()
        if not name:
            return jsonify({'error': 'Name parameter is required'}), 400
        
        users = UserService.search_users_by_name(name)
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': 'Search failed'}), 500