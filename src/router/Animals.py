from flask.views import MethodView
from flask import jsonify, request
from flasgger import swag_from
from src.models.Models import db, AnimalModel
from src.services.AuthService import Authentication
class AnimalView(MethodView):
    @swag_from({
    'tags': ['Animal'],
    'parameters': [
        {
            'name': 'animal_id',
            'in': 'path',
            'type': 'integer',
            'required': False,
            'description': 'ID of the animal to retrieve'
        }
    ],
    'security': [{'Bearer': []}],  # Include Bearer token authentication
    'responses': {
        200: {
            'description': 'Animal(s) retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'count': {
                        'type': 'integer',
                        'description': 'Number of animals returned',
                        'example': 5
                    },
                    'Animals': {
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
            }
        },
        404: {
            'description': 'Animal not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': 'Animal not found'
                    }
                }
            }
        }
    }
})
    @Authentication.token_required
    def get(self, current_user, animal_id=None):
        fields = ['id', 'name', 'species', 'age', 'special_requirement']
        
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
        'tags': ['Animal'],
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
        'security': [{'Bearer': []}],  # Include Bearer token authentication
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
                        'Animal': {
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
    @Authentication.token_required
    def post(self, current_user):
        data = request.get_json()

        fields = ['id','name', 'species', 'age', 'special_requirement']

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
            "Animal": animal_data
        }), 201
    
    @swag_from({
        'tags': ['Animal'],
        'parameters': [
            {
                'name': 'animal_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the animal to update'
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
                    }
                }
            }
        ],
        'security': [{'Bearer': []}],  # Include Bearer token authentication
        'responses': {
            200: {
                'description': 'Animal updated successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Animal updated successfully'
                        },
                        'animal': {
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
            404: {
                'description': 'Animal not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Animal not found'
                        }
                    }
                }
            }
        }
    })
    @Authentication.token_required
    def put(self, current_user, animal_id):
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
            "animal": animal_data,
        })
    

    @swag_from({
        'tags': ['Animal'],
        'parameters': [
            {
                'name': 'animal_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the animal to delete'
            }
        ],
        'security': [{'Bearer': []}],  # Include Bearer token authentication
        'responses': {
            200: {
                'description': 'Animal deleted successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Animal deleted successfully'
                        }
                    }
                }
            },
            404: {
                'description': 'Animal not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Animal not found'
                        }
                    }
                }
            }
        }
    })
    @Authentication.token_required
    def delete(self,current_user, animal_id):
        animal = AnimalModel.query.get(animal_id)
        if not animal:
            return jsonify({"error": "Animal not found"}), 404

        db.session.delete(animal)
        db.session.commit()
        return jsonify({"message": "Animal deleted successfully"})
    
