from flask import request, jsonify
from flask_restx import Resource, fields
from app.models import db, House, Car, Employer
from datetime import datetime

def register_routes(api):
    house_model = api.model('House', {
        'id': fields.Integer(readOnly=True),
        'name': fields.String(required=True),
        'sqrft': fields.Integer(required=True),
        'layout': fields.String(required=True)
    })

    delete_model = api.model('Delete', {
        'id': fields.Integer(required=True)
    })

    # House CRUD
    @api.route('/house')
    class HouseResource(Resource):
        @api.expect(house_model, validate=True)
        def post(self):
            data = request.json
            new = House(name=data['name'], sqrft=data['sqrft'], layout=data['layout'])
            db.session.add(new)
            db.session.commit()
            return {"message": "House added"}

        def get(self):
            return [h.to_dict() for h in House.query.all()]

        @api.expect(house_model, validate=True)
        def put(self):
            data = request.json
            h = House.query.get(data['id'])
            if h:
                h.name = data['name']
                h.sqrft = data['sqrft']
                h.layout = data['layout']
                db.session.commit()
                return {"message": "House updated"}
            return {"message": "Not found"}, 404

        @api.expect(delete_model, validate=True)
        def delete(self):
            data = request.json
            h = House.query.get(data['id'])
            if h:
                db.session.delete(h)
                db.session.commit()
                return {"message": "House deleted"}
            return {"message": "Not found"}, 404

    # Similar pattern can be followed for Car and Employer
