from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from decorators import auth_required, admin_required
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        page = request.args.get("page")

        filters = {"page": page}

        rs = director_service.get_all(filters)
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        request_json = request.json
        director = director_service.create(request_json)
        return '', 201, {'location': f'/directors/{director.id}'}


@director_ns.route('/<int:pk>')
class DirectorView(Resource):
    @auth_required
    def get(self, pk):
        r = director_service.get_one(pk)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, pk):
        request_json = request.json
        if 'id' not in request_json:
            request_json['id'] = pk

        director_service.update(request_json)
        return '', 204

    @admin_required
    def delete(self, pk):
        director_service.delete(pk)
        return '', 204
