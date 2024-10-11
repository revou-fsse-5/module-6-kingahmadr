import pytest
from unittest.mock import patch
from src.models.Models import AnimalTestModel
from src.config.settings import create_app, db

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
def appjson() -> dict:
    return {"Content-Type": "application/json"}