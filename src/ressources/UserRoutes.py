import falcon
from json import dumps


class Users:
    def on_get_email(self, req, resp):
        resp.status = falcon.HTTP_200
        if req.params:
            resp.media = req.params['id']
        else:
            resp.media = {'Message': 'Hello my friend'}

    def on_get_name(self, req, resp, name):
        resp.status = falcon.HTTP_200
        resp.media = {'Message': 'Hello World ' + name}

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {'Message': 'Hello World '}

    def on_post(self, req, resp):
        # récupérer le json
        raw_json = req.media

        resp.status = falcon.HTTP_200
        # renvoyer le json
        resp.body = dumps(raw_json)
