import falcon
from src.utils import enum
from src.data.db import Db
from datetime import datetime, timezone
from src.utils.logging import logger
from src.models.posts import Post
from src.utils.OpenAI import OpenAI


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
        self.db = Db.getInstance()

    def createPost(self, postObject):
        if OpenAI.moderateContent(postObject.text):
            raise falcon.HTTPForbidden("Forbidden", "Text contains offensive language")

        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute("INSERT INTO youshare.posts(id_user, id_url,text,date_published)"
                    " VALUES (%s,%s,%s,%s) RETURNING id_post,id_user,id_url,state,date_published,date_deleted, text",
                    [postObject.id_user, postObject.id_url, postObject.text, datetime.now(timezone.utc)])

        post_tuple = cur.fetchone()
        post = Post.from_tuple(post_tuple)

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return post

    def readOne(self, id_post):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute("SELECT id_post,id_user,id_url,state,date_published,date_deleted, text "
                    "FROM youshare.posts WHERE id_post = %s", [id_post])

        post_tuple = cur.fetchone()

        if post_tuple is None:
            logger.warn('Not Found The post is not registered yet')
            raise falcon.HTTPNotFound('Not Found', 'The post is not registered yet')

        post = Post.from_tuple(post_tuple)
        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return post

    def readMyPosts(self, id_user):
        cur = None
        conn = None
        try:
            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute(
                "SELECT id_post,id_user,id_url,state,date_published,date_deleted, text "
                "FROM youshare.posts WHERE id_user = %s "
                "ORDER BY date_published LIMIT 50; "
                , [id_user]
            )

            posts = cur.fetchall()
            listPost = []

            for post in posts:
                p = Post.from_tuple(post)
                listPost.append(p)

        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return listPost

    def readFeed(self, id_user):
        cur = None
        conn = None
        try:
            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute(
                "SELECT id_post,id_user,id_url,state,date_published,date_deleted, text FROM youshare.posts WHERE id_user = %s "
                "OR id_post IN (SELECT id_post FROM youshare.likes WHERE id_user IN "
                "(SELECT us.id_user FROM youshare.friendships as fr, youshare.users as us "
                "WHERE CASE WHEN fr.id_asker = %s THEN us.id_user = id_receiver ELSE us.id_user = id_asker END "
                "AND (fr.id_asker = %s OR fr.id_receiver = %s) "
                "AND fr.state = %s )) "
                "OR id_post IN (SELECT id_post FROM youshare.shares WHERE id_user IN "
                "(SELECT us.id_user "
                "FROM youshare.friendships as fr, youshare.users as us "
                "WHERE CASE WHEN fr.id_asker = %s THEN us.id_user = id_receiver ELSE us.id_user = id_asker END "
                "AND (fr.id_asker = %s OR fr.id_receiver = %s) "
                "AND fr.state = %s )) "
                "OR id_post IN (SELECT id_post FROM youshare.posts WHERE id_user IN "
                "(SELECT us.id_user "
                "FROM youshare.friendships as fr, youshare.users as us "
                "WHERE CASE WHEN fr.id_asker = %s THEN us.id_user = id_receiver ELSE us.id_user = id_asker END "
                "AND (fr.id_asker = %s OR fr.id_receiver = %s) "
                "AND fr.state = %s )) "
                "ORDER BY date_published LIMIT 50; ",
                [id_user, id_user, id_user, id_user, enum.STATE_ACCEPTED,
                 id_user, id_user, id_user, enum.STATE_ACCEPTED,
                 id_user, id_user, id_user, enum.STATE_ACCEPTED]
                )

            posts = cur.fetchall()
            listPost = []

            for post in posts:
                p = Post.from_tuple(post)
                listPost.append(p)

        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return listPost
