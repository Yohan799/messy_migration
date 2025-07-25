class UserNotFoundError(Exception):
    """Raised when a user is not found"""
    pass

class EmailExistsError(Exception):
    """Raised when trying to create/update user with existing email"""
    pass

class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass