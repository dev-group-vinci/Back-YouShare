import falcon

class Users(object):
    def on_get(self,req,resp):
        resp.status = falcon.HTTP_200
        resp.media = {'Message': 'Hello World'}