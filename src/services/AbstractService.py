import falcon
from src.data.db import Db
from src.utils.logging import logger
from src.services.PostsService import PostService


class AbstractService:
    __instance = None

    @staticmethod
    def getInstance():
        if AbstractService.__instance is None:
            AbstractService()
        return AbstractService.__instance

    def __init__(self):
        if AbstractService.__instance is not None:
            raise Exception("UserService instance already exist !!")
        else:
            AbstractService.__instance = self
        db = Db.getInstance()
        self.postServices = PostService.getInstance()
        self.conn = db.conn

    def add(self, table, id_post, id_user):
        cur = None
        try:
            self.postServices.readOne(id_post)

            if self.isAlreadyPresent(table, id_post, id_user):
                logger.warning("Post : {} is already done for user : {}".format(id_post, id_user))
                raise falcon.HTTPConflict

            cur = self.conn.cursor()

            cur.execute(" INSERT INTO youshare.{} (id_post, id_user)".format(table) +
                        " VALUES (%s,%s)", [id_post, id_user])

            self.conn.commit()
        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err
        cur.close()

        return self.readNbItem(table, id_post)

    def remove(self, table, id_post, id_user):
        cur = None
        try:
            self.postServices.readOne(id_post)

            if not self.isAlreadyPresent(table, id_post, id_user):
                logger.warning("Post : {} is already done for user : {}".format(id_post, id_user))
                raise falcon.HTTPConflict

            cur = self.conn.cursor()

            cur.execute(" DELETE FROM youshare.{}".format(table) +
                        " WHERE id_post = %s AND id_user = %s", [id_post, id_user])

            self.conn.commit()
        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err
        cur.close()

        return self.readNbItem(table, id_post)

    def readNbItem(self, table, id_post):
        cur = None
        try:

            cur = self.conn.cursor()

            cur.execute(" SELECT COUNT(*) as num_item"
                        " FROM youshare.{}".format(table) +
                        " WHERE id_post = %s ", [id_post])

            self.conn.commit()
        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err

        num_items = cur.fetchone()[0]
        cur.close()

        return num_items

    def isAlreadyPresent(self, table, id_post, id_user):
        cur = None
        try:
            self.postServices.readOne(id_post)
            cur = self.conn.cursor()
            cur.execute(" SELECT *"
                        " FROM youshare.{}".format(table) +
                        " WHERE id_post = %s AND id_user = %s", [id_post, id_user])

            item = cur.fetchone()
            self.conn.commit()

        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err

        cur.close()
        return item is not None
