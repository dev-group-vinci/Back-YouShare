import falcon


class Users:
    def on_get_email(self,req,resp):
        resp.status = falcon.HTTP_200
        resp.media = req.params['id']

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {'Message': 'Hello World'}



