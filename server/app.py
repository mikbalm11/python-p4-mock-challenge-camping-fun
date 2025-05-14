#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        campers = [camper.to_dict(rules=('-signups',)) for camper in Camper.query.all()]

        result = make_response(
            campers,
            200
        )
        return result

    def post(self):
        try:
            new_camper = Camper(
                name=request.json['name'],
                age=request.json['age']
            )

            db.session.add(new_camper)
            db.session.commit()

            result = make_response(
                new_camper.to_dict(rules=('-signups',)),
                201
            )

            return result
        except ValueError:
            result = make_response(
                {"errors": ["validation errors"]},
                400
            )

            return result

api.add_resource(Campers, "/campers")

class CampersById(Resource):
    def get(self, id):
        camper = Camper.query.filter(Camper.id == id).first()

        if camper is None:
            result = make_response(
                {'error': 'Camper not found'},
                404
            )
            return result

        result = make_response(
            camper.to_dict(),
            200
        )

        return result 

    def patch(self, id):
        camper = Camper.query.filter(Camper.id == id).first()

        if camper is None:
            result = make_response(
                {'error': 'Camper not found'},
                404
            )
            return result

        fields = request.get_json()

        try:
            setattr(camper, 'name', fields['name'])
            setattr(camper, 'age', fields['age'])
            db.session.add(camper)
            db.session.commit()

            result = make_response(
                camper.to_dict(rules=('-signups',)),
                202
            )
            return result

        except ValueError:
            result = make_response(
                {"errors": ["validation errors"]},
                400
            )

            return result

api.add_resource(CampersById, "/campers/<int:id>")

class Activities(Resource):
    def get(self):
        activities = [activity.to_dict(rules=('-signups',)) for activity in Activity.query.all()]

        result = make_response(
            activities,
            200
        )
        return result

api.add_resource(Activities, "/activities")

class ActivityById(Resource):
    def delete(self, id):
        activity = Activity.query.filter(Activity.id == id).first()

        if activity is None:
            result = make_response(
                {'error': 'Activity not found'},
                404
            )
            return result

        db.session.delete(activity)
        db.session.commit()

        result = make_response(
            '',
            204
        )

        return result

api.add_resource(ActivityById, "/activities/<int:id>")

class Signups(Resource):
    def post(self):
        try:
            new_signup = Signup(
                time=request.json["time"],
                camper_id=request.json["camper_id"],
                activity_id=request.json["activity_id"]
            )

            db.session.add(new_signup)
            db.session.commit()

            result = make_response(
                new_signup.to_dict(),
                201
            )

            return result

        except ValueError:
            result = make_response(
                {"errors": ["validation errors"]},
                400
            )
            return result

api.add_resource(Signups, "/signups")

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(port=5555, debug=True)
