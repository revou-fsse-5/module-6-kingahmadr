import pytest
import jwt
import os
from unittest.mock import patch, MagicMock
from src.models.Models import AnimalTestModel, EmployeeTestModel, User
from src.config.settings import create_app, db
from datetime import datetime, timedelta, timezone
from flask import request

# Mock environment variable
os.environ['JWT_SECRET'] = 'test_secret_key'

@pytest.fixture
def mock_user():
    # This fixture will mock a user object
    user = MagicMock()
    user.id = 1
    return user

@pytest.fixture
def mock_request_headers(mocker):
    # This fixture will mock the request object with a valid token
    mocker.patch('src.services.AuthService.request')  # Adjust the import path
    request.headers = {
        'Authorization': 'Bearer test_token'
    }

@pytest.fixture
def mock_jwt_token(mock_user):
    # Generate a mock JWT token for the user
    payload = {
        'user_id': mock_user.id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')



@pytest.fixture
def admin_username():
    return "admin"

@pytest.fixture(scope="module")
def app():
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture(scope="module")
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def test_db(app):
    db.create_all()
    yield db

@pytest.fixture
def generate_fake_animals(test_db):
    # Bersihin data dulu sebelum di generate animal dari test
    db.session.query(AnimalTestModel).delete()  # Hapus semua data animal di db
    db.session.commit()

    lion = AnimalTestModel(
        name="Lion",
        species="Panthera leo",
        age=5,
        special_requirement="Requires open space"
    )
    elephant = AnimalTestModel(
        name="Elephant",
        species="Loxodonta africana",
        age=10,
        special_requirement="Requires a lot of water"
    )
    
    cheetah = AnimalTestModel(
        name="Cheetah",
        species="Acinonyx jubatus",
        age=4,
        special_requirement="Needs wide open spaces"
    )
    
    test_db.session.add(lion)
    test_db.session.add(elephant)
    test_db.session.add(cheetah)
    test_db.session.commit()

    return [lion, elephant, cheetah]

@pytest.fixture
def generate_fake_employees(test_db):
    # Bersihin data dulu sebelum di generate animal dari test
    db.session.query(EmployeeTestModel).delete()  # Hapus semua data animal di db
    db.session.commit()

    robert = EmployeeTestModel(
        name="robert",
        email="robert@email.com",
        phone="3213900--321313-3123",
        role="Second Gatekeeper",
        schedule="Night Shift"
    )
    junior = EmployeeTestModel(
        name="junior",
        email="junior@email.com",
        phone="3213900--321313-3123",
        role="Second Gatekeeper",
        schedule="Night Shift"
    )
    edward = EmployeeTestModel(
        name="edward",
        email="edward@email.com",
        phone="3213900--321313-3123",
        role="Main Gatekeeper",
        schedule="Day Shift"
    )
    
    test_db.session.add(robert)
    test_db.session.add(junior)
    test_db.session.add(edward)
    test_db.session.commit()

    return [robert, junior, edward]

@pytest.fixture
def appjson() -> dict:
    return {"Content-Type": "application/json"}