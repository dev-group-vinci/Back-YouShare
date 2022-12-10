import falcon
from src.data.db import Db
from datetime import datetime, timezone
from src.utils.logging import logger
from src.services.PostsService import PostService
from src.services.AbstractService import AbstractService
from src.utils import enum

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

