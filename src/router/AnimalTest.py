from flask.views import MethodView
from flask import jsonify, request
from flasgger import swag_from
from src.models.Models import AnimalTestModel
from src.config.settings import db
from src.services.AuthService import Authentication

class AnimalViewTest(MethodView):
    def get(self, animal_id=None):
        fields = ['id', 'name', 'species', 'age', 'special_requirement']
        
        if animal_id is None:
            animals = AnimalTestModel.query.all()
            results = [{field: getattr(animal, field) for field in fields} for animal in animals]
            return jsonify({"count": len(results), "Animals": results})
            # return jsonify(results)
        else:
            animal = db.session.get(AnimalTestModel, animal_id)
            if not animal:
                return jsonify({"error": "Animal not found"}), 404

            animal_data = {field: getattr(animal, field) for field in fields}
            return jsonify(animal_data)
        
    def post(self):
        data = request.get_json()

        fields = ['id','name', 'species', 'age', 'special_requirement']

        required_fields = ['name', 'species', 'age']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing Required attribute: {field}"}), 400

        new_animal = AnimalTestModel()

        for field in fields:
            setattr(new_animal, field, data.get(field, None))

        db.session.add(new_animal)
        db.session.commit()

        animal_data = {field: getattr(new_animal, field) for field in fields}

        return jsonify({
            "message": "Animal data created successfully",
            "Animal": animal_data
        }), 201
    
    def put(self, animal_id):
        animal = db.session.get(AnimalTestModel, animal_id)
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

    def delete(self, animal_id):
        animal = db.session.get(AnimalTestModel, animal_id)
        if not animal:
            return jsonify({"error": "Animal not found"}), 404

        db.session.delete(animal)
        db.session.commit()
        return jsonify({"message": "Animal deleted successfully"})