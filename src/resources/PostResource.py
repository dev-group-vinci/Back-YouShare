import json

import falcon
from falcon.media.validators import jsonschema
from src.media import load_schema
from src.utils.Authenticate import Authenticate
from src.utils import enum
from src.services.PostsService import PostService
from json import dumps
from src.utils.json import datetime_to_iso_str

auth = Authenticate.getInstance()


class Posts:

    def __init__(self):
        self.postServices = PostService.getInstance()

    @jsonschema.validate(load_schema("new_post"))
    @falcon.before(auth, enum.ROLE_USER)
    def on_post(self, req, resp):
        # récupérer le json
        raw_json = req.media

        id_user = req.context.user.id_user

        newPost = self.postServices.createPost(id_user, raw_json['id_url'], raw_json['text'])

        resp.status = falcon.HTTP_201
        resp.body = dumps(newPost, default=datetime_to_iso_str)

    @falcon.before(auth, enum.ROLE_USER)
    def on_get_post(self, req, resp, id_post):
        post = self.postServices.readOne(id_post)

        resp.status = falcon.HTTP_200
        resp.body = dumps(post, default=datetime_to_iso_str)

    @falcon.before(auth, enum.ROLE_USER)
    def on_post_like(self, req, resp, id_post):
        id_user = req.context.user.id_user
        nb_like = self.postServices.like(id_post, id_user)

        resp.status = falcon.HTTP_201
        resp.body = dumps(nb_like, default=int)
