from src.utils import enum
from src.services.PostsService import PostService
from src.services.AbstractService import AbstractService

class LikeService:
    __instance = None

    @staticmethod
    def getInstance():
        if LikeService.__instance is None:
            LikeService()
        return LikeService.__instance

    def __init__(self):
        if LikeService.__instance is not None:
            raise Exception("UserService instance already exist !!")
        else:
            LikeService.__instance = self
        self.postServices = PostService.getInstance()
        self.abstractService = AbstractService.getInstance()

    def like(self, id_post, id_user):
        return self.abstractService.add(enum.LIKE_TABLE, id_post, id_user)

    def unlike(self, id_post, id_user):
        return self.abstractService.remove(enum.LIKE_TABLE, id_post, id_user)

    def readNbLike(self, id_post):
        return self.abstractService.readNbItem(enum.LIKE_TABLE, id_post)

