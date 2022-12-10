import hashlib
import base64
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, pk):
        return self.dao.get_one(pk)

    def get_all(self):
        return self.dao.get_all()

    def get_by_email(self, email):
        return self.dao.get_by_username(email)

    def create(self, user_d):
        user_d['password'] = self.make_password_hash(user_d.get('password'))
        return self.dao.create(user_d)

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def delete(self, pk):
        self.dao.delete(pk)

    def make_password_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_passwords(self, password_hash, request_password):
        request_password_hash = base64.b64encode(hashlib.pbkdf2_hmac('sha256',
                                                                     request_password.encode('utf-8'),
                                                                     PWD_HASH_SALT,
                                                                     PWD_HASH_ITERATIONS))
        return hmac.compare_digest(password_hash, request_password_hash)
