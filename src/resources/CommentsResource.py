import falcon

from src.utils.Authenticate import Authenticate
from src.utils import enum
from src.utils.json import datetime_to_iso_str
from src.models.comments import Comment
from src.services.CommentService import CommentService
from json import dumps
from src.media import load_schema
from falcon.media.validators import jsonschema

auth = Authenticate.getInstance()


class Comments:

    def __init__(self):
        self.commentServices = CommentService.getInstance()

    @falcon.before(auth, enum.ROLE_USER)
    def on_get(self, req, resp, id_post):
        comments = self.commentServices.readCommentsPost(id_post)

        resp.status = falcon.HTTP_200
        resp.body = dumps(comments, default=datetime_to_iso_str)

    @falcon.before(auth, enum.ROLE_USER)
    def on_post(self, req, resp):
        id_user = req.context.user['id_user']

        raw_json = req.media
        comment = Comment()
        comment.create_new_comment_from_json(raw_json)
        comment.id_user = id_user
        if comment.id_comment_parent == -1:
            comment.id_comment_parent = None
        comment = self.commentServices.addComment(comment)

        resp.status = falcon.HTTP_201
        resp.body = dumps(comment, default=datetime_to_iso_str)

    @falcon.before(auth, enum.ROLE_USER)
    def on_delete(self, req, resp, id_post):
        id_user = req.context.user['id_user']

        self.commentServices.deleteAllCommentsPost(id_post, id_user)

        resp.status = falcon.HTTP_202

    @jsonschema.validate(load_schema("new_comment"))
    @falcon.before(auth, enum.ROLE_USER)
    def on_delete_one(self, req, resp, id_comment):
        id_user = req.context.user['id_user']

        self.commentServices.deleteOneCommentPost(id_comment, id_user)

        resp.status = falcon.HTTP_202
