import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from src.models.Models import db

from src.router.Routes import AnimalView, EmployeeView

app = Flask(__name__)
# load_dotenv()

# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres.rxagpymjyxdlnaweylcz:{os.getenv('PASSWORD')}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}@{os.getenv('HOST_DB')}:{os.getenv('PORT_DB')}/{os.getenv('DBNAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration
db.init_app(app)
migrate = Migrate(app, db)

animal_view = AnimalView.as_view('animal_view')
app.add_url_rule('/v2/animal', defaults={'animal_id': None}, view_func=animal_view, methods=['GET'])
app.add_url_rule('/v2/animal/<int:animal_id>', view_func=animal_view, methods=['GET'])
app.add_url_rule('/v2/animal/add', view_func=animal_view, methods=['POST'])
app.add_url_rule('/v2/animal/edit/<int:animal_id>', view_func=animal_view, methods=['PUT'])
app.add_url_rule('/v2/animal/delete/<int:animal_id>', view_func=animal_view, methods=['DELETE'])

employee_view = EmployeeView.as_view('employee_view')
app.add_url_rule('/v2/employee', defaults={'employee_id': None}, view_func=employee_view, methods=['GET'])
app.add_url_rule('/v2/employee/<int:employee_id>', view_func=employee_view, methods=['GET'])
app.add_url_rule('/v2/employee/add', view_func=employee_view, methods=['POST'])
app.add_url_rule('/v2/employee/edit/<int:employee_id>', view_func=employee_view, methods=['PUT'])
app.add_url_rule('/v2/employee/delete/<int:employee_id>', view_func=employee_view, methods=['DELETE'])

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