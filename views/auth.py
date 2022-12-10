from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service, user_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class RegisterView(Resource):
    def post(self):
        request_json = request.json
        email = request_json.get('email')
        password = request_json.get('password')

        if None in [email, password]:
            return '', 400

        request_json['favorite_genre'] = 1
        user_service.create(request_json)

        return 'User created', 201


@auth_ns.route('/login')
class AuthService(Resource):
    def post(self):
        request_json = request.json

        email = request_json.get('email')
        password = request_json.get('password')

        if None in [email, password]:
            return '', 400

        tokens = auth_service.generate_token(email, password)
        return tokens, 201

    def put(self):
        req_json = request.json
        access_token = req_json.get('access_token')
        refresh_token = req_json.get('refresh_token')
        valid = auth_service.valid_token(access_token, refresh_token)
        if not valid:
            return 'Invalid token', 400
        tokens = auth_service.check_token(refresh_token)

        return tokens, 201
