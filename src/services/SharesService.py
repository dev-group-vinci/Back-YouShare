import falcon
from src.data.db import Db
from datetime import datetime, timezone
from src.utils.logging import logger
from src.services.PostsService import PostService


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
        db = Db.getInstance()
        self.postServices = PostService.getInstance()
        self.conn = db.conn

    def share(self, id_post, id_user):
        cur = None
        try:
            self.postServices.readOne(id_post)

            if self.isShared(id_post, id_user):
                logger.warning("Post : {} is already Shared for user : {}".format(id_post, id_user))
                raise falcon.HTTPConflict

            cur = self.conn.cursor()

            cur.execute(" INSERT INTO youshare.shares (id_post, id_user)"
                        " VALUES (%s,%s)", [id_post, id_user])

            self.conn.commit()
        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err
        cur.close()

        return self.readNbShare(id_post)

    def unshare(self, id_post, id_user):
        cur = None
        try:
            self.postServices.readOne(id_post)

            if not self.isShared(id_post, id_user):
                logger.warning("Post : {} is already unshared for user : {}".format(id_post, id_user))
                raise falcon.HTTPConflict

            cur = self.conn.cursor()

            cur.execute(" DELETE FROM youshare.shares"
                        " WHERE id_post = %s AND id_user = %s", [id_post, id_user])

            self.conn.commit()
        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err
        cur.close()

        return self.readNbShare(id_post)

    def readNbShare(self, id_post):
        cur = None
        try:

            cur = self.conn.cursor()

            cur.execute(" SELECT COUNT(*) as num_shared"
                        " FROM youshare.shares"
                        " WHERE id_post = %s ", [id_post])

            self.conn.commit()
        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err

        num_shares = cur.fetchone()[0]
        cur.close()

        return num_shares

    def isShared(self, id_post, id_user):
        cur = None
        try:
            self.postServices.readOne(id_post)
            cur = self.conn.cursor()
            cur.execute(" SELECT *"
                        " FROM youshare.shares"
                        " WHERE id_post = %s AND id_user = %s", [id_post, id_user])

            share = cur.fetchone()
            self.conn.commit()

        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err

        cur.close()
        return share is not None
