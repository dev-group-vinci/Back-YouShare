import falcon
from src.data.db import Db
from datetime import datetime, timezone
from src.utils.logging import logger
from src.services.PostsService import PostService

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
        db = Db.getInstance()
        self.postServices = PostService.getInstance()
        self.conn = db.conn

    def like(self, id_post, id_user):
        cur = None
        try:
            self.postServices.readOne(id_post)

            if self.isLiked(id_post, id_user):
                logger.warning("Post : {} is already liked for user : {}".format(id_post, id_user))
                raise falcon.HTTPConflict

            cur = self.conn.cursor()

            cur.execute(" INSERT INTO youshare.likes (id_post, id_user)"
                        " VALUES (%s,%s)", [id_post, id_user])

            cur.execute(" SELECT COUNT(*) as num_likes"
                        " FROM youshare.likes"
                        " WHERE id_post = %s ", [id_post])

            self.conn.commit()
        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err

        num_likes = cur.fetchone()[0]
        cur.close()

        return num_likes

    def isLiked(self, id_post, id_user):
        cur = None
        try:
            self.postServices.readOne(id_post)
            cur = self.conn.cursor()
            cur.execute(" SELECT *"
                        " FROM youshare.likes"
                        " WHERE id_post = %s AND id_user = %s", [id_post, id_user])

            like = cur.fetchone()
            self.conn.commit()

        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err

        cur.close()
        return like is not None
