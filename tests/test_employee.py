def test_create_employee(client, mock_jwt_token):

    headers = {
        'Authorization': f'Bearer {mock_jwt_token}',
        'Content-Type': 'application/json'
    }


    """Test creating a new employee via POST /v2/employee"""
    new_employee = {
        "name": "Gabriel",
        "email": "gabriel@email.com",
        "phone": "3213128300-455",
        "role": "Second Gate keeper",
        "schedule": "Swing Shift"
    }

    response = client.post('/v2/employee', json=new_employee, headers=headers)
    assert response.status_code == 201

    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Employee data created successfully"

def test_get_all_employees(client, mock_jwt_token):
    """Test retrieving all employees via GET /v2/employee"""
    headers = {
        'Authorization': f'Bearer {mock_jwt_token}',
       
    }

    response = client.get('/v2/employee',headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    
    # Check that data is a dictionary
    assert isinstance(data, dict)

    # Check that the "count" and "employees" keys exist in the response
    assert "count" in data
    assert "Employees" in data

    # Check that "employees" is a list and "count" matches the length of that list
    assert isinstance(data["Employees"], list)
    assert data["count"] == len(data["Employees"])

def test_get_employee_by_id(client, generate_fake_employees, mock_jwt_token):
    """Test retrieving an employee by its ID via GET /v2/employee<id>"""

    headers = {
        'Authorization': f'Bearer {mock_jwt_token}'
    }

    robert = generate_fake_employees[0]  # Get the first employee (robert)
    response = client.get(f'/v2/employee/{robert.id}', headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data['id'] == robert.id
    assert data['name'] == "robert"


def test_update_employee(client, generate_fake_employees, mock_jwt_token):
    """Test updating an existing employee via PUT /v2/employee/<id>"""
    headers = {
        'Authorization': f'Bearer {mock_jwt_token}',
        'Content-Type': 'application/json'
    }

    robert = generate_fake_employees[0]  # Get the first employee (Robert)
    updated_data = {"schedule": "Night shift"}

    response = client.put(f'/v2/employee/{robert.id}', json=updated_data, headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "employee updated successfully"

def test_delete_employee(client, generate_fake_employees,mock_jwt_token):
    """Test deleting an employee via DELETE /v2/employee/<id>"""
    headers = {
        'Authorization': f'Bearer {mock_jwt_token}',
        'Content-Type': 'application/json'
    }
    edward = generate_fake_employees[0]  # Get the first employee (Lion)

    response = client.delete(f'/v2/employee/{edward.id}',headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "employee deleted successfully"

    # Ensure the employee was actually deleted
    response = client.get(f'/v2/employee/{edward.id}',headers=headers)
    assert response.status_code == 404