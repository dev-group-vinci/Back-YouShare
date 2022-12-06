from wsgiref.simple_server import make_server
import falcon

class HelloWorldJson(object):
    def on_get(self,req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {'Message' : 'Hello World'}

class HelloWorldText(object):
    def on_get(self, req , resp):
        resp.status = falcon.HTTP_200
        resp.body = "Hello World"

if __name__ == '__main__':
    api = falcon.App()
    api.add_route('/json', HelloWorldJson())
    api.add_route('/text', HelloWorldText())
    print("Server started")
    with make_server('',8080,api) as httpd:
        httpd.serve_forever()
