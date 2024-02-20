from functools import wraps
from flask import request
from utils.jwt_utils import verify_jwt
from utils.rsa_key_utils import load_public_key

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract JWT token from request headers
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing'}, 401

        # Extract the JWT token from the Authorization header
        token = token.split(' ')[1] if token.startswith('Bearer ') else token

        # Load public key
        public_key = load_public_key()

        # Verify the JWT token
        result = verify_jwt(token, public_key)
        
        if 'error' in result:
            return {'message': 'Forbidden, JWT invalid'}, 403
        
        return func(*args, **kwargs)

    return wrapper
