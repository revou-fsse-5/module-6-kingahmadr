from flask.views import MethodView
from flask import jsonify, request
from flasgger import swag_from
from src.models.Models import User
from src.services.AuthService import Authentication

from werkzeug.security import generate_password_hash, check_password_hash

class AuthView(MethodView):
    @swag_from({
    'tags': ['Authentication'],  # You can adjust the tag name
    'summary': 'User login',
    'description': 'Login endpoint that authenticates a user and returns a JWT token.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'Email and password for login',
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string',
                        'example': 'user@example.com'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'password123'
                    }
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful, JWT token returned',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Login successful!'
                    },
                    'token': {
                        'type': 'string',
                        'example': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid email or password',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': 'Invalid email or password!'
                    }
                }
            }
        }
    }
})
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid email or password!"}), 400
        
        # Generate JWT token for the user
        token = Authentication.create_jwt_token(user.id)

        
        return jsonify({
            "message": "Login successful!",
            "token": token  # Send the token to the client
        }), 200