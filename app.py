import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from src.models.Models import db
from flasgger import Swagger

from src.router.Animals import AnimalView
from src.router.Employees import EmployeeView
from src.router.Swagger import SwaggerView

app = Flask(__name__)
swagger = Swagger(app)
# Swagger config for securityDefinitions
# app.config['SWAGGER'] = {
#     'securityDefinitions': {
#         'Bearer': {
#             'type': 'apiKey',
#             'name': 'Authorization',
#             'in': 'header',
#             'description': 'Enter JWT with **Bearer** prefix, e.g., "Bearer {token}"'
#         }
#     },
#     'security': [
#         {
#             'Bearer': []
#         }
#     ]
# }
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