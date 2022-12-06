from wsgiref.simple_server import make_server
import falcon

from ressources.UserRoutes import Users


class HelloWorldJson:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {'Message': 'Hello World'}


class HelloWorldText:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = "Hello World"


if __name__ == '__main__':
    api = falcon.App(cors_enable=True)

    api.add_route('/json', HelloWorldJson())
    api.add_route('/text', HelloWorldText())
    api.add_route('/users', Users())
    api.add_route('/users/email', Users(), suffix='email')
    print("Server started")
    with make_server('', 8080, api) as httpd:
        httpd.serve_forever()
