import falcon
from src.data.db import Db
from datetime import datetime, timezone
from src.utils.logging import logger
from src.models.posts import Post


class PostService:
    __instance = None

    @staticmethod
    def getInstance():
        if PostService.__instance is None:
            PostService()
        return PostService.__instance

    def __init__(self):
        if PostService.__instance is not None:
            raise Exception("UserService instance already exist !!")
        else:
            PostService.__instance = self
        db = Db.getInstance()
        self.conn = db.conn

    def createPost(self, id_user, id_url, text):
        cur = self.conn.cursor()

        cur.execute("INSERT INTO youshare.posts(id_user, id_url,text,date_published)"
                    " VALUES (%s,%s,%s,%s) RETURNING id_post,id_user,id_url,state,date_published,text",
                    [id_user, id_url, text, datetime.now(timezone.utc)])

        post_tuple = cur.fetchone()
        post = Post.from_tuple(post_tuple)

        self.conn.commit()
        cur.close()
        return post

    def readOne(self, id_post):
        cur = self.conn.cursor()

        cur.execute("SELECT id_post,id_user,id_url,state,text,date_published,date_deleted"
                    " FROM youshare.posts WHERE id_post = %s", [id_post])

        post_tuple = cur.fetchone()

        if post_tuple is None:
            logger.warn('Not Found The post is not registered yet')
            raise falcon.HTTPNotFound('Not Found', 'The post is not registered yet')

        post = Post.from_tuple(post_tuple)
        self.conn.commit()
        cur.close()

        return post
