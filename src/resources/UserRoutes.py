import base64

import falcon
from json import dumps
from falcon.media.validators import jsonschema
from src.media import load_schema
from src.utils.Authenticate import Authenticate
from src.services.UsersService import UserService

auth = Authenticate()

class Users:
    def __init__(self, conn):
        self.userServices = UserService(conn=conn)


    def on_get_email(self, req, resp):
        resp.status = falcon.HTTP_200
        if req.params:
            resp.media = req.params['id']
        else:
            resp.media = {'Message': 'Hello my friend'}

    def on_get_name(self, req, resp, name):
        resp.status = falcon.HTTP_200
        resp.media = {'Message': 'Hello World ' + name}

    @falcon.before(auth, "admin")
    def on_get(self, req, resp):
        print(req.context.user)
        resp.status = falcon.HTTP_200
        resp.media = {'Message': 'Hello World '}

    @jsonschema.validate(load_schema('user_register'))
    @falcon.before(auth, "user")
    def on_post(self, req, resp):

        # récupérer le json
        raw_json = req.media

        resp.status = falcon.HTTP_200
        # renvoyer le json
        resp.body = dumps(raw_json)

    @jsonschema.validate(load_schema('user_login'))
    def on_post_login(self, req, resp):
        raw_json = req.media
        id = self.userServices.login(raw_json['email'],raw_json['password'])
        token = auth.encode(id_user=int(id))
        resp.status = falcon.HTTP_200
        resp.body = dumps({
            'token': token
        })

    @jsonschema.validate(load_schema('user_register'))
    def on_post_register(self, req, resp):
        # récupérer le json
        raw_json = req.media
        resp.status = falcon.HTTP_200
        id = self.userServices.registerUser(raw_json['email'], raw_json['username'], raw_json['password'])

        token = auth.encode(id_user=int(id))
        # renvoyer le json
        resp.body = dumps(token)
