import falcon
from falcon.media.validators import jsonschema
from src.media import load_schema
from src.utils.Authenticate import Authenticate
from src.utils import enum
from src.services.CommentService import CommentService
from json import dumps

auth = Authenticate()


class Comments:

    def __init__(self):
        self.commentServices = CommentService.getInstance()

    @falcon.before(auth, enum.ROLE_USER)
    def on_get(self, req, resp, id_post):
        comments = self.commentServices.readCommentsPost(id_post)

        resp.status = falcon.HTTP_200
        resp.body = dumps(comments)
