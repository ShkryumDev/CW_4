from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        request_json = request.json
        user = user_service.create(request_json)
        return '', 201, {'location': f'/users/{user.id}'}


@user_ns.route('/<int:pk>')
class UserView(Resource):
    def get(self, pk):
        r = user_service.get_one(pk)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def put(self, pk):
        request_json = request.json
        if 'id' not in request_json:
            request_json['id'] = pk

        user_service.update(request_json)
        return '', 204

    def delete(self, pk):
        user_service.delete(pk)
        return '', 204

