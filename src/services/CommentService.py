import falcon
from src.models.comments import Comment
from src.data.db import Db
from datetime import datetime, timezone
from src.utils.logging import logger
from src.services.PostsService import PostService
from src.utils import enum
from src.utils.OpenAI import OpenAI


class CommentService:
    __instance = None

    @staticmethod
    def getInstance():
        if CommentService.__instance is None:
            CommentService()
        return CommentService.__instance

    def __init__(self):
        if CommentService.__instance is not None:
            raise Exception("UserService instance already exist !!")
        else:
            CommentService.__instance = self
        self.db = Db.getInstance()
        self.postServices = PostService.getInstance()

    def readCommentsPost(self, id_post):
        cur = None
        conn = None

        self.postServices.readOne(id_post)

        try:

            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute(
                "SELECT c.id_comment, c.id_user, c.id_post,"
                " c.id_comment_parent, c.text, c.state, c.date_published,"
                " c.date_deleted FROM youshare.comments c, youshare.posts p"
                " WHERE c.id_post = %s AND c.id_post = p.id_post", [id_post]
            )

            comments = cur.fetchall()
            listComment = []

            for comment in comments:
                c = Comment.from_tuple(comment)
                listComment.append(c)

        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return listComment

    def addComment(self, commentObject):
        cur = None
        conn = None

        if OpenAI.moderateContent(commentObject.text):
            raise falcon.HTTPForbidden("Forbidden", "Text contains offensive language")

        post = self.postServices.readOne(commentObject.id_post)
        if post.state == enum.POST_DELETED:
            logger.warning("The post is actually deleted you can't comment it")
            raise falcon.HTTPForbidden("The post is actually deleted you can't comment it")

        if commentObject is not None:
            try:
                self.readOneComment(commentObject.id_comment_parent)
            except BaseException as error:
                logger.info("No comment parent found")
                pass

        try:

            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO youshare.comments (id_user, id_post,"
                " id_comment_parent, text, state) VALUES (%s,%s,%s,%s,%s)"
                "RETURNING id_comment, id_user, id_post,"
                " id_comment_parent, text, state, date_published,"
                " date_deleted"
                , [commentObject.id_user, commentObject.id_post,
                   commentObject.id_comment_parent, commentObject.text,
                   enum.COMMENT_PUBLISHED]
            )

            comment_tuple = cur.fetchone()
            comment = Comment.from_tuple(comment_tuple)

        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return comment

    def deleteAllCommentsPost(self, id_post, id_ownerPost_user):
        cur = None
        conn = None

        post = self.postServices.readOne(id_post)

        if post.id_user != id_ownerPost_user:
            logger.warning("You are not available to delete all comment of this post")
            raise falcon.HTTPForbidden("Not identified as the corresponding user")

        try:

            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute(
                "UPDATE youshare.comments SET state = %s, date_deleted = %s "
                "WHERE id_post = %s ", [enum.COMMENT_DELETED, datetime.now(timezone.utc), id_post]
            )

        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()

    def deleteOneCommentPost(self, id_post, id_comment, id_ownerPost_user):
        cur = None
        conn = None

        self.postServices.readOne(id_post)
        comment = self.readOneComment(id_comment)

        if comment.id_user != id_ownerPost_user:
            logger.warning("You are not available to delete this comment ")
            raise falcon.HTTPForbidden("Not identified as the corresponding user")

        try:

            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute(
                "UPDATE youshare.comments SET state = %s, date_deleted = %s "
                "WHERE id_comment = %s AND id_post = %s "
                "RETURNING id_comment, id_user, id_post, "
                "id_comment_parent, text, state, date_published, "
                "date_deleted"
                , [enum.COMMENT_DELETED, datetime.now(timezone.utc), id_comment, id_post]
            )

            comment_tuple = cur.fetchone()
            comment = Comment.from_tuple(comment_tuple)
        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return comment

    def readOneComment(self, id_comment):
        cur = None
        conn = None
        try:
            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute(
                " SELECT *"
                " FROM youshare.comments"
                " WHERE id_comment = %s", [id_comment]
            )

            comment_tuple = cur.fetchone()

            if comment_tuple is None:
                logger.warn('Not Found The comment is not registered yet')
                raise falcon.HTTPNotFound('Not Found', 'The comment is not registered yet')

            comment = Comment.from_tuple(comment_tuple)

        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return comment
