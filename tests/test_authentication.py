import pytest
import jwt
import os
from flask import jsonify, request
from unittest.mock import patch
from src.services.AuthService import Authentication  # Import your module
from src.models.Models import User

os.environ['JWT_SECRET'] = 'test_secret_key'
# Test for create_jwt_token method
def test_create_jwt_token(mock_user):
    token = Authentication.create_jwt_token(mock_user.id)
    
    # Decode the token to ensure correctness
    decoded = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
    
    assert decoded['user_id'] == mock_user.id
    assert 'exp' in decoded

# Test for token_required decorator (valid token)
@patch('src.config.settings.db.session.get')  # Adjust import for User
def test_token_required_valid_token(mock_get, mock_jwt_token, mock_user, app, client):
    # Mock User query to return the mock user
    mock_get.return_value = mock_user
    
    # Mock wrapped function
    def mock_view_function(user, *args, **kwargs):
        return jsonify({"message": "Success"}), 200

    # Wrap the mock view function with the token_required decorator
    decorated_function = Authentication.token_required(mock_view_function)

    # Simulate a request with a valid token using Flask test client
    headers = {
        'Authorization': f'Bearer {mock_jwt_token}'
    }

    with client.application.test_request_context(headers=headers):
        response = decorated_function()
    
    # Verify the function was called and the user was passed
    assert response[1] == 200
    assert response[0].json['message'] == 'Success'

# Test for token_required decorator (missing token)
def test_token_required_missing_token(app, client):
    def mock_view_function(user, *args, **kwargs):
        return jsonify({"message": "Success"}), 200
    
    decorated_function = Authentication.token_required(mock_view_function)
    
    with client.application.test_request_context(headers={}):
        response = decorated_function()
    
    assert response[1] == 403
    assert response[0].json['error'] == "Token is missing!"

# Test for token_required decorator (invalid token)
@patch('src.services.AuthService.jwt.decode')  # Adjust the path for jwt.decode
def test_token_required_invalid_token(mock_decode, app, client):
    # Mock jwt.decode to raise InvalidTokenError
    mock_decode.side_effect = jwt.InvalidTokenError("Invalid token")
    
    def mock_view_function(user, *args, **kwargs):
        return jsonify({"message": "Success"}), 200

    headers = {
        'Authorization': 'Bearer invalid_token'
    }
    
    decorated_function = Authentication.token_required(mock_view_function)
    
    with client.application.test_request_context(headers=headers):
        response = decorated_function()
    
    assert response[1] == 403
    assert response[0].json['error'] == "Invalid token!"