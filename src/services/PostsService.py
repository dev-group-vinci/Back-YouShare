import falcon
from src.data.db import Db
from datetime import datetime, timezone


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
                    " VALUES (%s,%s,%s,%s) RETURNING id_video,id_url,state,date_published,text",
                    [id_user, id_url, text, datetime.now(timezone.utc)])

        row = cur.fetchone()
        print("row ::: ", row)

        self.conn.commit()
        cur.close()
        return row

    def readOne(self, id_post):
        cur = self.conn.cursor()

        cur.execute("SELECT id_video,id_url,state,text,date_published,date_deleted"
                    " FROM youshare.posts WHERE id_video = %s", [id_post])

        post = cur.fetchone()

        self.conn.commit()
        cur.close()

        if post is None:
            raise falcon.HTTPNotFound('Not Found', 'The post is not registered yet')

        return post
