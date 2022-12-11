import falcon
from src.models.comments import Comment
from src.data.db import Db
from src.utils.logging import logger
from src.services.PostsService import PostService


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
        db = Db.getInstance()
        self.postServices = PostService.getInstance()
        self.conn = db.conn

    def readCommentsPost(self, id_post):
        cur = None
        try:

            self.postServices.readOne(id_post)

            cur = self.conn.cursor()

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
            self.conn.rollback()
            logger.warning(err)
            raise err

        self.conn.commit()
        cur.close()
        return listComment

    def addComment(self, commentObject):
        cur = None
        try:

            self.postServices.readOne(commentObject.id_post)

            cur = self.conn.cursor()

            cur.execute(
                "INSERT INTO youshare.comments (id_user, id_post,"
                " id_comment_parent, text, state) VALUES (%s,%s,%s,%s,%s)"
                "RETURNING id_comment, id_user, id_post,"
                " id_comment_parent, text, state, date_published,"
                " date_deleted"
                , [commentObject.id_user, commentObject.id_post,
                   commentObject.id_comment_parent, commentObject.text,
                   commentObject.state]
            )

            comment_tuple = cur.fetchone()
            comment = Comment.from_tuple(comment_tuple)
            print("comment :: ", comment.text)
        except BaseException as err:
            self.conn.rollback()
            logger.warning(err)
            raise err

        self.conn.commit()
        cur.close()
        return comment
