import json

import falcon
from falcon.media.validators import jsonschema
from src.media import load_schema
from src.utils.Authenticate import Authenticate
from src.utils import enum
from src.services.PostsService import PostService
from src.services.LikesService import LikeService
from json import dumps

auth = Authenticate()


class Likes:

    def __init__(self):
        self.likeServices = LikeService.getInstance()

    @falcon.before(auth, enum.ROLE_USER)
    def on_post(self, req, resp, id_post):
        id_user = req.context.user['id_user']
        nb_like = self.likeServices.like(id_post, id_user)

        resp.status = falcon.HTTP_201
        resp.body = dumps(nb_like, default=int)

    @falcon.before(auth, enum.ROLE_USER)
    def on_get(self, req, resp, id_post):
        nb_like = self.likeServices.readNbLike(id_post)

        resp.status = falcon.HTTP_201
        resp.body = dumps(nb_like, default=int)

    @falcon.before(auth, enum.ROLE_USER)
    def on_delete(self, req, resp, id_post):
        id_user = req.context.user['id_user']
        nb_like = self.likeServices.unlike(id_post, id_user)

        resp.status = falcon.HTTP_201
        resp.body = dumps(nb_like, default=int)
