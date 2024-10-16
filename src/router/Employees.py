from flask.views import MethodView
from flask import jsonify, request
from flasgger import swag_from
from src.models.Models import db, EmployeeModel
from src.services.AuthService import Authentication

class EmployeeView(MethodView):
    @swag_from({
        'tags': ['Employee'],
        'parameters': [
            {
                'name': 'employee_id',
                'in': 'path',
                'type': 'integer',
                'required': False,
                'description': 'ID of the employee to retrieve'
            }
        ],
        'security': [{'Bearer': []}],  # Include Bearer token authentication
        'responses': {
            200: {
                'description': 'Employees(s) retrieved successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'count': {
                            'type': 'integer',
                            'description': 'Number of employee returned',
                            'example': 5
                        },
                        'Employee': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'id': {
                                        'type': 'integer',
                                        'example': 1
                                    },
                                    'name': {
                                        'type': 'string',
                                        'example': 'jonathan'
                                    },
                                    'email': {
                                        'type': 'string',
                                        'example': 'jonathan@email.com'
                                    },
                                    'phone': {
                                        'type': 'string',
                                        'example': '000-213-893882'
                                    },
                                    'role': {
                                        'type': 'string',
                                        'example': 'Main keeper'
                                    },
                                    'schedule': {
                                        'type': 'string',
                                        'example': 'Night Shift'
                                    }
                                }
                            }
                        }
                    }
                }
            },
            404: {
                'description': 'Employee not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Employee not found'
                        }
                    }
                }
            }
        }
    })
    @Authentication.token_required
    def get(self,current_user, employee_id=None):
        fields = ['id','name', 'email', 'phone', 'role', 'schedule']
        if employee_id is None:
            employees = EmployeeModel.query.all()

            results = [{field: getattr(employee, field) for field in fields} for employee in employees]
            return jsonify({"count": len(results), "Employees": results})
        else:
            employee = db.session.get(EmployeeModel, employee_id)
            if not employee:
                return jsonify({"error": "Employee not found"}), 404

            employee_data = {field: getattr(employee, field) for field in fields}
            return jsonify(employee_data)

    @swag_from({
        'tags': ['Employee'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'Name of the employee',
                            'example': 'Leo'
                        },
                        'email': {
                            'type': 'string',
                            'description': 'Emial of the employee',
                            'example': 'jonathan@email.com'
                        },
                        'phone': {
                            'type': 'string',
                            'description': 'Age of the employee',
                            'example': '000-2313-32455656'
                        },
                        'role': {
                            'type': 'string',
                            'description': 'Role of the employee',
                            'example': 'Main keeper'
                        },
                        'schedule': {
                            'type': 'string',
                            'description': 'Schedule of the staff',
                            'example': 'Night Shift'
                        }
                    },
                    'required': ['name', 'email', 'role']  # Required fields
                }
            }
        ],
        'security': [{'Bearer': []}],  # Include Bearer token authentication
        'responses': {
            201: {
                'description': 'employee data created successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'employee data created successfully'
                        },
                        'employee': {
                            'type': 'object',
                            'properties': {
                                'name': {
                                    'type': 'string',
                                    'example': 'Jonathan'
                                },
                                'email': {
                                    'type': 'string',
                                    'example': 'jonathan@email.com'
                                },
                                'phone': {
                                    'type': 'string',
                                    'example': '000-313123-98890'
                                },
                                'role': {
                                    'type': 'string',
                                    'example': 'Main keeper'
                                },
                                'schedule': {
                                    'type': 'string',
                                    'example': 'Night Shift'
                                }
                            }
                        }
                    }
                }
            },
            400: {
                'description': 'Missing required attribute',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Missing Required attribute: name'
                        }
                    }
                }
            }
        }
    })
    @Authentication.token_required
    def post(self, current_user):
        data = request.get_json()

        fields = ['name', 'email', 'phone', 'role', 'schedule']

        required_fields = ['name', 'email', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing Required attribute: {field}"}), 400

        new_employee = EmployeeModel()

        for field in fields:
            setattr(new_employee, field, data.get(field, None))

        db.session.add(new_employee)
        db.session.commit()

        employee_data = {field: getattr(new_employee, field) for field in fields}

        return jsonify({
            "message": "Employee data created successfully",
            "employee": employee_data
        }), 201

    @swag_from({
        'tags': ['Employee'],
        'parameters': [
            {
                'name': 'employee_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the employee to update'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'Name of the employee',
                            'example': 'Jonathan'
                        },
                        'email': {
                            'type': 'string',
                            'description': 'Species of the employee',
                            'example': 'jonathan@email.com'
                        },
                        'phone': {
                            'type': 'string',
                            'description': 'Phone of the employee',
                            'example': '000-233120-30123123'
                        },
                        'schedule': {
                            'type': 'string',
                            'description': 'Schedule of the staff',
                            'example': 'Night Shift'
                        }
                    }
                }
            }
        ],
        'security': [{'Bearer': []}],  # Include Bearer token authentication
        'responses': {
            200: {
                'description': 'Employee updated successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Employee updated successfully'
                        },
                        'employee': {
                            'type': 'object',
                            'properties': {
                                'name': {
                                    'type': 'string',
                                    'description': 'Name of the employee',
                                    'example': 'Jonathan'
                                },
                                'email': {
                                    'type': 'string',
                                    'description': 'Species of the employee',
                                    'example': 'jonathan@email.com'
                                },
                                'phone': {
                                    'type': 'string',
                                    'description': 'Phone of the employee',
                                    'example': '000-233120-30123123'
                                },
                                'schedule': {
                                    'type': 'string',
                                    'description': 'Schedule of the staff',
                                    'example': 'Night Shift'
                                }
                            }
                        }
                    }
                }
            },
            404: {
                'description': 'Employee not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Employee not found'
                        }
                    }
                }
            }
        }
    })
    @Authentication.token_required
    def put(self,current_user, employee_id):
        employee = db.session.get(EmployeeModel, employee_id)
        if not employee:
            return jsonify({"error": "employee not found"}), 404
        
        fields = ['name', 'email', 'phone', 'role', 'schedule']

        for field in fields:
            value = request.json.get(field)
            if value:
                setattr(employee, field, value)

        db.session.commit()
        employee_data = {field: getattr(employee, field) for field in fields}

        return jsonify({
            "message": "employee updated successfully",
            "employee": employee_data,
        })
    
    @swag_from({
        'tags': ['Employee'],
        'parameters': [
            {
                'name': 'employee_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the employee to delete'
            }
        ],
        'security': [{'Bearer': []}],  # Include Bearer token authentication
        'responses': {
            200: {
                'description': 'Employee deleted successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Employee deleted successfully'
                        }
                    }
                }
            },
            404: {
                'description': 'Employee not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Employee not found'
                        }
                    }
                }
            }
        }
    })
    @Authentication.token_required
    def delete(self,current_user, employee_id):
        employee = db.session.get(EmployeeModel, employee_id)
        if not employee:
            return jsonify({"error": "employee not found"}), 404

        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "employee deleted successfully"})