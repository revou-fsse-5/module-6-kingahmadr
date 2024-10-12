from flask.views import MethodView
from flask import jsonify, request
from src.models.Models import EmployeeTestModel
from src.config.settings import db

class EmployeeViewTest(MethodView):
    def get(self, employee_id=None):
        fields = ['id','name', 'email', 'phone', 'role', 'schedule']
        
        if employee_id is None:
            employees = EmployeeTestModel.query.all()
            results = [{field: getattr(employee, field) for field in fields} for employee in employees]
            return jsonify({"count": len(results), "Employees": results})
            # return jsonify(results)
        else:
            employee = db.session.get(EmployeeTestModel, employee_id)
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

        new_employee = EmployeeTestModel()

        for field in fields:
            setattr(new_employee, field, data.get(field, None))

        db.session.add(new_employee)
        db.session.commit()

        employee_data = {field: getattr(new_employee, field) for field in fields}

        return jsonify({
            "message": "Employee data created successfully",
            "employee": employee_data
        }), 201
    
    def put(self, employee_id):
        employee = db.session.get(EmployeeTestModel, employee_id)
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
            "message": "Employee updated successfully",
            "employee": employee_data,
        })

    def delete(self, employee_id):
        employee = db.session.get(EmployeeTestModel, employee_id)
        if not employee:
            return jsonify({"error": "employee not found"}), 404

        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "employee deleted successfully"})