from src.utils import enum
from src.services.PostsService import PostService
from src.services.AbstractService import AbstractService

class ShareService:
    __instance = None

    @staticmethod
    def getInstance():
        if ShareService.__instance is None:
            ShareService()
        return ShareService.__instance

    def __init__(self):
        if ShareService.__instance is not None:
            raise Exception("UserService instance already exist !!")
        else:
            ShareService.__instance = self
        self.postServices = PostService.getInstance()
        self.abstractService = AbstractService.getInstance()

    def share(self, id_post, id_user):
        return self.abstractService.add(enum.SHARE_TABLE, id_post, id_user)

    def unshare(self, id_post, id_user):
        return self.abstractService.remove(enum.SHARE_TABLE, id_post, id_user)

    def readNbShare(self, id_post):
        return self.abstractService.readNbItem(enum.SHARE_TABLE, id_post)

