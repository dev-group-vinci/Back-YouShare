import falcon
from json import dumps
from src.utils import enum
from src.utils.Authenticate import Authenticate
from src.services.SharesService import ShareService

auth = Authenticate.getInstance()


class Shares:

    def __init__(self):
        self.shareServices = ShareService.getInstance()

    @falcon.before(auth, enum.ROLE_USER)
    def on_post(self, req, resp, id_post):
        id_user = req.context.user.id_user
        nb_share = self.shareServices.share(id_post, id_user)

        resp.status = falcon.HTTP_201
        resp.body = dumps(nb_share, default=int)

    @falcon.before(auth, enum.ROLE_USER)
    def on_get(self, req, resp, id_post):
        nb_share = self.shareServices.readNbShare(id_post)

        resp.status = falcon.HTTP_201
        resp.body = dumps(nb_share, default=int)

    @falcon.before(auth, enum.ROLE_USER)
    def on_delete(self, req, resp, id_post):
        id_user = req.context.user.id_user
        nb_share = self.shareServices.unshare(id_post, id_user)

        resp.status = falcon.HTTP_201
        resp.body = dumps(nb_share, default=int)
