import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from src.models.Models import db
from flasgger import Swagger

from src.router.Animals import AnimalView
from src.router.Employees import EmployeeView
from src.router.Swagger import SwaggerView
from src.router.Auth import AuthView
from src.router.Register import RegisterView

app = Flask(__name__)
# Swagger configuration for securityDefinitions
swagger_config = {
    "swagger": "2.0",
    "title": "Your API Title",
    "description": "API documentation with JWT authentication",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ],
    # Include the 'specs' key to resolve KeyError
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",  # URL for accessing the Swagger UI
    # Add a headers key to prevent TypeError
    "headers": []
}

swagger = Swagger(app, config=swagger_config)
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}@{os.getenv('HOST_DB')}:{os.getenv('PORT_DB')}/{os.getenv('DBNAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Initialize the database and migration
db.init_app(app)
migrate = Migrate(app, db)

animal_view = AnimalView.as_view('animal_view')
app.add_url_rule('/v2/animal', view_func=animal_view, methods=['GET', 'POST'])
app.add_url_rule('/v2/animal/<int:animal_id>', view_func=animal_view, methods=['GET','DELETE', 'PUT'])

employee_view = EmployeeView.as_view('employee_view')
app.add_url_rule('/v2/employee', view_func=employee_view, methods=['GET', 'POST'])
app.add_url_rule('/v2/employee/<int:employee_id>', view_func=employee_view, methods=['GET', 'DELETE', 'PUT'])

swagger_view = SwaggerView.as_view('swagger_view')
app.add_url_rule('/v2/swagger', view_func=swagger_view, methods=['GET'])

auth_view = AuthView.as_view('auth_view')
app.add_url_rule('/v2/login', view_func=auth_view, methods=['POST'])

register_view = RegisterView.as_view('register_view')
app.add_url_rule('/v2/register', view_func=register_view, methods=['POST'])





@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/v1/value')
def get_value():
    result = f"print {os.getenv('HOST_DB')} + {os.getenv('USER_DB')}"
    # result = f"postgresql://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}@{os.getenv('HOST_DB')}:{os.getenv('PORT_DB')}/{os.getenv('DBNAME')}"
    return result

# Main driver function
if __name__ == '__main__':
    app.run()