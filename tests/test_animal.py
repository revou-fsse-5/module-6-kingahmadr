def test_get_all_animals(client, generate_fake_animals):
    """Test retrieving all animals via GET /v2/test/animal"""
    response = client.get('/v2/test/animal')
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

def test_get_animal_by_id(client, generate_fake_animals):
    """Test retrieving an animal by its ID via GET /v2/test/animal<id>"""
    lion = generate_fake_animals[0]  # Get the first animal (Lion)
    response = client.get(f'/v2/test/animal/{lion.id}')
    assert response.status_code == 200

    data = response.get_json()
    assert data['id'] == lion.id
    assert data['name'] == "Lion"

def test_create_animal(client, appjson):
    """Test creating a new animal via POST /v2/test/animal"""
    new_animal = {
        "name": "Giraffe",
        "species": "Giraffa camelopardalis",
        "age": 8,
        "special_requirement": "Needs tall trees"
    }

    response = client.post('/v2/test/animal', json=new_animal, headers=appjson)
    assert response.status_code == 201

    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Animal data created successfully"

def test_update_animal(client, generate_fake_animals, appjson):
    """Test updating an existing animal via PUT /v2/test/animal/<id>"""
    lion = generate_fake_animals[0]  # Get the first animal (Lion)
    updated_data = {"habitat": "Rainforest"}

    response = client.put(f'/v2/test/animal/{lion.id}', json=updated_data, headers=appjson)
    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Animal updated successfully"

def test_delete_animal(client, generate_fake_animals):
    """Test deleting an animal via DELETE /v2/test/animal/<id>"""
    lion = generate_fake_animals[0]  # Get the first animal (Lion)

    response = client.delete(f'/v2/test/animal/{lion.id}')
    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Animal deleted successfully"

    # Ensure the animal was actually deleted
    response = client.get(f'/v2/test/animal/{lion.id}')
    assert response.status_code == 404