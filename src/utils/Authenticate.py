import falcon
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()


class Authenticate(object):
    def encode(self, idUser, username):
        now = datetime.utcnow()
        payload = {
            'id': idUser,
            'username': username,
            'iat': now,
            'exp': (now + timedelta(hours=24)).timestamp()
        }

        token = jwt.encode(
            payload=payload,
            key=os.getenv("jwt_secret"),
            algorithm="HS256"
        )

        return token

    def decode_and_validate_token(self, access_token):
        unverified_headers = jwt.get_unverified_header(access_token)
        return jwt.decode(
            access_token,
            key=os.getenv("jwt_secret"),
            algorithms=unverified_headers['alg']
        )

    def __auth_basic(self, username, password):
        if True:
            print("You have access")
        else:
            raise falcon.HTTPUnauthorized('Unauthorized', 'You have no access')

    def __call__(self, req, resp, resource, params, role):

        print("Before trigger - class: Authorize")
        # token = req.get_header('Authorization')
        token = self.encode(1, "mehdi");

        try:
            decodedToken = self.decode_and_validate_token(token)
        except jwt.exceptions.DecodeError as err:
            raise falcon.HTTPUnauthorized('Unauthorized', 'Token expired')

        req.context.user = decodedToken['id']

        if token:
            pass
        else:
            raise falcon.HTTPNotImplemented('Not Implemented', 'Please specify a token')
