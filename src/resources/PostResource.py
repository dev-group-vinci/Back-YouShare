import json

import falcon
from falcon.media.validators import jsonschema
from src.media import load_schema
from src.utils.Authenticate import Authenticate
from src.utils import enum
from src.services.PostsService import PostService
from json import dumps

auth = Authenticate()


class Posts:

    def __init__(self):
        self.postServices = PostService.getInstance()

    @jsonschema.validate(load_schema("new_post"))
    @falcon.before(auth, enum.ROLE_USER)
    def on_post(self, req, resp):
        # récupérer le json
        raw_json = req.media

        id_user = req.context.user['id']

        newPost = self.postServices.createPost(id_user, raw_json['id_url'], raw_json['text'])

        resp.status = falcon.HTTP_201
        resp.body = dumps({
            'id_video': newPost[0],
            'id_url': newPost[1],
            'state': newPost[2],
            'date_published': newPost[3],
            'text': newPost[4],
        }, default=str)
