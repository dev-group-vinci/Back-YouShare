import falcon
import jwt
from datetime import datetime, timedelta
import os
from src.utils import enum

from src.utils.logging import logger
from src.services.UsersService import UserService


class Authenticate(object):

    def __int__(self):
        pass

    def encode(self, id_user):
        now = datetime.utcnow()
        payload = {
            'id': id_user,
            'iat': now,
            'exp': (now + timedelta(hours=24)).timestamp()
        }

        token = jwt.encode(
            payload=payload,
            key=os.getenv("JWT_SECRET"),
            algorithm="HS256"
        )

        return token

    def decode_and_validate_token(self, access_token):
        return jwt.decode(
            access_token,
            key=os.getenv("JWT_SECRET"),
            algorithms=["HS256"]
        )

    def __call__(self, req, resp, resource, params, role):

        logger.info("Authorize for " + role)
        token = req.get_header('Authorization')

        if not token:
            logger.warning("No token specified")
            raise falcon.HTTPUnauthorized('Unauthorized', 'Please specify a token')


        try:
            decodedToken = self.decode_and_validate_token(token)
        except jwt.exceptions.DecodeError as err:
            logger.warning("Token expired " + err)
            raise falcon.HTTPUnauthorized('Unauthorized', 'Token expired')

        userService = UserService.getInstance()
        user = userService.getUser(decodedToken['id'])

        if user['role'] != role and user['role'] == enum.ROLE_USER:
            logger.warning("Unauthorized access")
            raise falcon.HTTPNotAcceptable('Not Acceptable', 'Not authenticated as an admin ')

        req.context.user = user