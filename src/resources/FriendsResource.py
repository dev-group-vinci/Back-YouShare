import falcon
from json import dumps
from falcon.media.validators import jsonschema
from src.media import load_schema
from src.utils.Authenticate import Authenticate
from src.services.FriendsService import FriendsService
from src.utils import enum

auth = Authenticate()


class Friends:
    def __init__(self):
        self.friendsService = FriendsService.getInstance()

    @falcon.before(auth, enum.ROLE_USER)
    def on_get(self, req, resp):
        list = self.friendsService.getAll(req.context.user['id_user'])

        resp.status = falcon.HTTP_200
        resp.body = dumps(list)


