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


@user_ns.route('/password')
class UpdateUserPasswordViews(Resource):
    def put(self):
        request_json = request.json

        email = request_json.get('email')
        old_password = request_json.get('password_1')
        new_password = request_json.get('password_2')

        user = user_service.get_by_email(email)

        if user_service.compare_passwords(user.password, old_password):
            user.password = user_service.make_password_hash(new_password)
            result = UserSchema().dump(user)
            user_service.update(result)
        else:
            print('Password did not changed')

        return '', 201


@user_ns.route('/<int:pk>')
class UserView(Resource):
    def get(self, pk):
        r = user_service.get_one(pk)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def patch(self, pk):
        request_json = request.json
        if 'id' not in request_json:
            request_json['id'] = pk

        user_service.update(request_json)
        return '', 204

    def delete(self, pk):
        user_service.delete(pk)
        return '', 204
