from flask.views import MethodView
from flask import jsonify, request
from src.models.Models import db, User
from flasgger import swag_from
# from src.services.AuthService import Authentication
from werkzeug.security import generate_password_hash, check_password_hash


class RegisterView(MethodView):
    @swag_from({
    'tags': ['Authentication'],  # Group under Authentication tag
    'summary': 'User registration',
    'description': 'Endpoint to register a new user with an email and password.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'Email and password for user registration',
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string',
                        'example': 'newuser@example.com'
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
        201: {
            'description': 'User registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'User registered successfully!'
                    }
                }
            }
        },
        400: {
            'description': 'User already exists or invalid input',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': 'User already exists!'
                    }
                }
            }
        }
    }
})
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # User checking in database
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User already exists!"}), 400

        # Hash the user's password and create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201


