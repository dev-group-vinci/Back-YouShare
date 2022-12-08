from wsgiref.simple_server import make_server
import falcon

from src.resources.UserRoutes import Users
from src.data.db import Db
from src.utils.logging import logger
import os


class HelloWorldJson:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {'Message': 'Hello World'}


class HelloWorldText:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = "Hello World"


if __name__ == '__main__':
    api = falcon.App(cors_enable=True, middleware=[])

    # database connection
    database = Db()
    database.connect()

    users = Users()
    api.add_route('/json', HelloWorldJson())
    api.add_route('/text', HelloWorldText())
    api.add_route('/users/', users)
    api.add_route('/users/{name}', users, suffix='name')
    api.add_route('/users/email', users, suffix='email')  # avec query param (id)
    api.add_route('/users/login', users, suffix='login')
    api.add_route('/users/register',users,suffix='register')

    logger.info("Server started")

    with make_server('', int(os.getenv("srv_port")) , api) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        logger.info("Server closed")
        database.close()
        httpd.server_close()
