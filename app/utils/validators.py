from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.user import User

class UserCreateSchema(Schema):
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Name is required'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required', 'invalid': 'Invalid email format'}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        error_messages={'required': 'Password is required', 'invalid': 'Password must be at least 8 characters'}
    )
    
    @validates('email')
    def validate_email_unique(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError('Email already exists')

class UserUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=100))
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=8))

class UserLoginSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required', 'invalid': 'Invalid email format'}
    )
    password = fields.Str(
        required=True,
        error_messages={'required': 'Password is required'}
    )
