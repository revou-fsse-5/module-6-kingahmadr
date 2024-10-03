from flask.views import MethodView
from flask import jsonify, request
from flasgger import swag_from
from src.models.Models import db, AnimalModel, EmployeeModel

class AnimalView(MethodView):
    @swag_from({
        'parameters': [
            {
                'name': 'animal_id',  
                'in': 'query',
                'type': 'integer',  
                'required': False,
                'description': 'Query the animal list by animal_id'
            }
        ],
        'responses': {
            200: {
                'description': 'Get animal list',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'greeting': {
                            'type': 'string',
                            'example': 'Animal list'
                        }
                    }
                }
            }
        }
    })
    def get(self,animal_id):
        # animal_id = request.args.get('animal_id')
        animal_params = request.args.get('animal_id')
        fields = ['id', 'name', 'species', 'age', 'special_requirement']

        if animal_params:    
            if animal_params is None:
                animals = AnimalModel.query.all()

                results = [{field: getattr(animal, field) for field in fields} for animal in animals]
                return jsonify({"count": len(results), "Animals": results})
            else:
                animal = AnimalModel.query.get(animal_params)
                if not animal:
                    return jsonify({"error": "Animal not found"}), 404

                animal_data = {field: getattr(animal, field) for field in fields}
                return jsonify(animal_data)
            
        if animal_id is None:
            animals = AnimalModel.query.all()

            results = [{field: getattr(animal, field) for field in fields} for animal in animals]
            return jsonify({"count": len(results), "Animals": results})
        else:
            animal = AnimalModel.query.get(animal_id)
            if not animal:
                return jsonify({"error": "Animal not found"}), 404

            animal_data = {field: getattr(animal, field) for field in fields}
            return jsonify(animal_data)
    
    @swag_from({
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
                            'description': 'Name of the animal',
                            'example': 'Leo'
                        },
                        'species': {
                            'type': 'string',
                            'description': 'Species of the animal',
                            'example': 'Lion'
                        },
                        'age': {
                            'type': 'integer',
                            'description': 'Age of the animal',
                            'example': 5
                        },
                        'special_requirement': {
                            'type': 'string',
                            'description': 'Any special requirements the animal has',
                            'example': 'Needs a large cage'
                        }
                    },
                    'required': ['name', 'species', 'age']  # Required fields
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Animal data created successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Animal data created successfully'
                        },
                        'employee': {
                            'type': 'object',
                            'properties': {
                                'name': {
                                    'type': 'string',
                                    'example': 'Leo'
                                },
                                'species': {
                                    'type': 'string',
                                    'example': 'Lion'
                                },
                                'age': {
                                    'type': 'integer',
                                    'example': 5
                                },
                                'special_requirement': {
                                    'type': 'string',
                                    'example': 'Needs a large cage'
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
    def post(self):
        data = request.get_json()

        fields = ['name', 'species', 'age', 'special_requirement']

        required_fields = ['name', 'species', 'age']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing Required attribute: {field}"}), 400

        new_animal = AnimalModel()

        for field in fields:
            setattr(new_animal, field, data.get(field, None))

        db.session.add(new_animal)
        db.session.commit()

        animal_data = {field: getattr(new_animal, field) for field in fields}

        return jsonify({
            "message": "Animal data created successfully",
            "employee": animal_data
        }), 201
    
    def put(self, animal_id):
        animal = AnimalModel.query.get(animal_id)
        if not animal:
            return jsonify({"error": "Animal not found"}), 404
        
        fields = ['name', 'species', 'age', 'special_requirement']

        for field in fields:
            value = request.json.get(field)
            if value:
                setattr(animal, field, value)

        db.session.commit()
        animal_data = {field: getattr(animal, field) for field in fields}

        return jsonify({
            "message": "Animal updated successfully",
            "employee": animal_data,
        })

    def delete(self, animal_id):
        animal = AnimalModel.query.get(animal_id)
        if not animal:
            return jsonify({"error": "Animal not found"}), 404

        db.session.delete(animal)
        db.session.commit()
        return jsonify({"message": "Animal deleted successfully"})
    
class EmployeeView(MethodView):
    def get(self, employee_id):
        fields = ['id','name', 'email', 'phone', 'role', 'schedule']
        if employee_id is None:
            employees = EmployeeModel.query.all()

            results = [{field: getattr(animal, field) for field in fields} for animal in employees]
            return jsonify({"count": len(results), "Employees": results})
        else:
            employee = EmployeeModel.query.get(employee_id)
            if not employee:
                return jsonify({"error": "Employee not found"}), 404

            employee_data = {field: getattr(employee, field) for field in fields}
            return jsonify(employee_data)
    
    def post(self):
        data = request.get_json()

        fields = ['name', 'email', 'phone', 'role', 'schedule']

        required_fields = ['name', 'email', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing Required attribute: {field}"}), 400

        new_animal = EmployeeModel()

        for field in fields:
            setattr(new_animal, field, data.get(field, None))

        db.session.add(new_animal)
        db.session.commit()

        animal_data = {field: getattr(new_animal, field) for field in fields}

        return jsonify({
            "message": "Animal data created successfully",
            "employee": animal_data
        }), 201
    
    def put(self, employee_id):
        employee = EmployeeModel.query.get(employee_id)
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

    def delete(self, employee_id):
        employee = EmployeeModel.query.get(employee_id)
        if not employee:
            return jsonify({"error": "employee not found"}), 404

        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "employee deleted successfully"})