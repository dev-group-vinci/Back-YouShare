import html
import falcon
from json import dumps
from src.utils import enum
from src.media import load_schema
from src.models.posts import Post
from falcon.media.validators import jsonschema
from src.utils.json import datetime_to_iso_str
from src.utils.Authenticate import Authenticate
from src.services.PostsService import PostService
from src.utils.json import parseList, parseElement

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
        post = Post().create_new_post_from_json(raw_json)

        post.id_user = id_user
        post.id_url = html.escape(post.id_url)
        post.text = html.escape(post.text)

        newPost = self.postServices.createPost(post)

        resp.status = falcon.HTTP_201
        resp.body = dumps(parseElement(newPost), default=datetime_to_iso_str)

    @falcon.before(auth, enum.ROLE_USER)
    def on_get(self, req, resp):
        id_user = req.context.user.id_user
        posts = self.postServices.readFeed(id_user)

        resp.status = falcon.HTTP_200
        resp.body = dumps(parseList(posts), default=datetime_to_iso_str)

    @falcon.before(auth, enum.ROLE_USER)
    def on_get_me(self, req, resp):
        id_user = req.context.user.id_user
        posts = self.postServices.readMyPosts(id_user)

        resp.status = falcon.HTTP_200
        resp.body = dumps(parseList(posts), default=datetime_to_iso_str)

    @falcon.before(auth, enum.ROLE_USER)
    def on_get_post(self, req, resp, id_post):
        post = self.postServices.readOne(id_post)

        resp.status = falcon.HTTP_200
        resp.body = dumps(parseElement(post), default=datetime_to_iso_str)

    @falcon.before(auth, enum.ROLE_USER)
    def on_post_like(self, req, resp, id_post):
        id_user = req.context.user.id_user
        nb_like = self.postServices.like(id_post, id_user)

        resp.status = falcon.HTTP_201
        resp.body = dumps(nb_like, default=int)

    @falcon.before(auth, enum.ROLE_USER)
    def on_delete(self, req, resp, id_post):
        user = req.context.user

        self.postServices.deleteOne(id_post, user)

        resp.status = falcon.HTTP_202
