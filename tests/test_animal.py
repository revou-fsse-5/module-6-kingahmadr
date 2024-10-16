
def test_create_animal(client, mock_jwt_token):

    headers = {
        'Authorization': f'Bearer {mock_jwt_token}',
        'Content-Type': 'application/json'
    }

    """Test creating a new animal via POST /v2/animal"""
    new_animal = {
        "name": "Giraffe",
        "species": "Giraffa camelopardalis",
        "age": 8,
        "special_requirement": "Needs tall trees"
    }

    response = client.post('/v2/animal', json=new_animal, headers=headers)
    assert response.status_code == 201

    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Animal data created successfully"

def test_get_all_animals(client, mock_jwt_token):
    headers = {
        'Authorization': f'Bearer {mock_jwt_token}'
    }

    """Test retrieving all animals via GET /v2/animal"""
    response = client.get('/v2/animal', headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    
    # Check that data is a dictionary
    assert isinstance(data, dict)

    # Check that the "count" and "Animals" keys exist in the response
    assert "count" in data
    assert "Animals" in data

    # Check that "Animals" is a list and "count" matches the length of that list
    assert isinstance(data["Animals"], list)
    assert data["count"] == len(data["Animals"])


def test_get_animal_by_id(client, generate_fake_animals, mock_jwt_token):
    """Test retrieving an animal by its ID via GET /v2/animal<id>"""
    headers = {
        'Authorization': f'Bearer {mock_jwt_token}'
    }
    lion = generate_fake_animals[0]  # Get the first animal (Lion)
    response = client.get(f'/v2/animal/{lion.id}',headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data['id'] == lion.id
    assert data['name'] == "Lion"

def test_update_animal(client, generate_fake_animals, mock_jwt_token):
    """Test updating an existing animal via PUT /v2/animal/<id>"""
    
    headers = {
        'Authorization': f'Bearer {mock_jwt_token}',
        'Content-Type': 'application/json'
    }
    lion = generate_fake_animals[0]  # Get the first animal (Lion)
    updated_data = {"special_requirement": "Rainforest"}

    response = client.put(f'/v2/animal/{lion.id}', json=updated_data, headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Animal updated successfully"

def test_delete_animal(client, generate_fake_animals, mock_jwt_token):
    """Test deleting an animal via DELETE /v2/animal/<id>"""
    headers = {
        'Authorization': f'Bearer {mock_jwt_token}',
        'Content-Type': 'application/json'
    }
    elephant = generate_fake_animals[1]  # Get the first animal (Lion)

    response = client.delete(f'/v2/animal/{elephant.id}',headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Animal deleted successfully"

    # Ensure the animal was actually deleted
    response = client.get(f'/v2/animal/{elephant.id}', headers=headers)
    assert response.status_code == 404