from flask.views import MethodView
from flask import jsonify, request
from flasgger import swag_from

class SwaggerView(MethodView):
    @swag_from({
            'tags': ['Example'],
            'parameters': [
                {
                    'name': 'name',
                    'in': 'query',
                    'type': 'string',
                    'required': True,
                    'description': 'The name of the user to greet'
                }
            ],
            'responses': {
                200: {
                    'description': 'A greeting to the user',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'greeting': {
                                'type': 'string',
                                'example': 'Hello, John!'
                            }
                        }
                    }
                }
            }
        })
    def get(self):
        """
        Greet a user
        """
        name = request.args.get('name')
        greeting = f"Hello, {name}!"
        return jsonify(greeting=greeting), 200
        