import falcon
import jwt
from datetime import datetime, timedelta
import os
from src.utils import enum

from src.data.db import Db
from src.utils.logging import logger


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

        logger.info("Authorize for "+role)
        token = req.get_header('Authorization')

        if not token:
            logger.warning("No token specified")
            raise falcon.HTTPNotImplemented('Not Implemented', 'Please specify a token')


        try:
            decodedToken = self.decode_and_validate_token(token)
        except jwt.exceptions.DecodeError as err:
            logger.warning("Token expired "+err)
            raise falcon.HTTPUnauthorized('Unauthorized', 'Token expired')

        db = Db.getInstance()
        cur = db.conn.cursor()

        cur.execute("SELECT * FROM youshare.users WHERE id_user=%s", [decodedToken['id']])
        data = cur.fetchone()

        db.conn.commit()
        cur.close()

        if data[2] != role and data[2] == enum.ROLE_USER:
            db.conn.commit()
            cur.close()
            logger.warning("Unauthorized access")
            raise falcon.HTTPUnauthorized('Unauthorized','You don\'t have the right to access this data')

        req.context.user = {
            "id":data[0],
            "username":data[1],
            "role":data[2],
            "email":data[3]
        }


