import bcrypt
import falcon
from src.data.db import Db
from src.utils import enum
from src.services.UsersService import UserService
from src.models.friends import Friends
from src.utils.logging import logger

class FriendsService:
    __instance = None

    @staticmethod
    def getInstance():
        if FriendsService.__instance is None:
            FriendsService()
        return FriendsService.__instance

    def __init__(self):
        if FriendsService.__instance is not None:
            raise Exception("UserService instance already exist !!")
        else:
            FriendsService.__instance = self
            self.userServices = UserService.getInstance()
            self.db = Db.getInstance()


    def getAll(self,id_user):
        cur = None
        conn = None

        try:
            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute(
                "SELECT fr.state,us.id_user,us.username,us.role,us.email,us.biography,us.picture "
                "FROM youshare.friendships as fr, youshare.users as us "
                "WHERE CASE WHEN fr.id_asker = %s THEN us.id_user = id_receiver ELSE us.id_user = id_asker END "
                "AND (fr.id_asker = %s OR fr.id_receiver = %s) "
                "AND fr.state = %s ",
                (id_user, id_user, id_user,enum.STATE_ACCEPTED)
            )

            # Récupérez les résultats de la requête
            friends = cur.fetchall()

            list = []

            # Affichez les amis de l'utilisateur et leur rôle (expéditeur ou destinataire)
            for friend in friends:
                user = Friends.from_tuple(friend)
                list.append(user)
        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return list

    def getAllFriendRequests(self,id_user):
        cur = None
        conn = None

        try:
            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute(
                "SELECT fr.state,us.id_user,us.username,us.role,us.email,us.biography,us.picture "
                "FROM youshare.friendships as fr, youshare.users as us "
                "WHERE us.id_user = id_asker "
                "AND fr.id_receiver = %s "
                "AND fr.state != %s ",
                (id_user, enum.STATE_ACCEPTED)
            )

            # Récupérez les résultats de la requête
            friends = cur.fetchall()

            list = []

            # Affichez les amis de l'utilisateur et leur rôle (expéditeur ou destinataire)
            for friend in friends:
                user = Friends.from_tuple(friend)
                list.append(user)
        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return list

    def getAllMyFriendRequests(self,id_user):
        cur = None
        conn = None

        try:
            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute(
                "SELECT fr.state,us.id_user,us.username,us.role,us.email,us.biography,us.picture "
                "FROM youshare.friendships as fr, youshare.users as us "
                "WHERE us.id_user = id_receiver "
                "AND fr.id_asker = %s "
                "AND fr.state != %s ",
                (id_user, enum.STATE_ACCEPTED)
            )

            # Récupérez les résultats de la requête
            friends = cur.fetchall()

            list = []

            # Affichez les amis de l'utilisateur et leur rôle (expéditeur ou destinataire)
            for friend in friends:
                user = Friends.from_tuple(friend)
                list.append(user)
        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return list

    def friendRequestExist(self,id_asker,id_receiver):
        cur = None
        conn = None

        try:
            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute("SELECT * FROM youshare.friendships WHERE (id_asker = %s AND id_receiver = %s) OR (id_asker = %s AND id_receiver = %s)", [id_asker, id_receiver,id_receiver,id_asker])
            row = cur.fetchone()
        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return row is not None


    def addFriendRequest(self,id_asker,id_receiver):
        if id_asker == id_receiver:
            raise falcon.HTTPForbidden("Forbidden","You cannot add yourself as a friend")
        if not self.userServices.userExist(id_receiver):
            raise falcon.HTTPNotFound("Not Found","User not found")
        if self.friendRequestExist(id_asker,id_receiver):
            raise falcon.HTTPConflict("Conflict","Friend request already exist")

        cur = None
        conn = None

        try:
            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute("INSERT INTO youshare.friendships(id_asker,id_receiver) VALUES (%s,%s)",[id_asker,id_receiver])
        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()

    def deleteFriendRequest(self,id_user,id_friend):

        if id_user == id_friend:
            raise falcon.HTTPForbidden("Forbidden", "You cannot delete yourself as a friend")
        if not self.userServices.userExist(id_friend):
            raise falcon.HTTPNotFound("Not Found", "User not found")
        if not self.friendRequestExist(id_user, id_friend):
            raise falcon.HTTPNotFound("Not Found", "Friend request don't exist")

        cur = None
        conn = None

        try:
            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute("DELETE FROM youshare.friendships WHERE (id_asker = %s AND id_receiver = %s) OR (id_asker = %s AND id_receiver = %s)", [id_user, id_friend,id_friend,id_user])
        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err
        conn.commit()
        cur.close()
        self.db.freeConnexion()

    def acceptFriendRequest(self,id_user,id_friend):
        if id_user == id_friend:
            raise falcon.HTTPForbidden("Forbidden", "You cannot accept yourself as a friend")
        if not self.userServices.userExist(id_friend):
            raise falcon.HTTPNotFound("Not Found", "User not found")
        if not self.friendRequestExist(id_user, id_friend):
            raise falcon.HTTPNotFound("Not Found", "Friend request don't exist")
        cur = None
        conn = None

        try:
            conn = self.db.getConnection()
            cur = conn.cursor()


            cur.execute("SELECT state FROM youshare.friendships WHERE id_receiver = %s AND id_asker = %s",[id_user,id_friend])
            state = cur.fetchone()
        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()

        if state is None:
            raise falcon.HTTPForbidden("Forbidden", "You cannot accept a friend request when you are the asker")
        elif state[0] == enum.STATE_ACCEPTED:
            raise falcon.HTTPConflict("Conflict", "Friend request already accepted")
        else:
            self.accept(id_user,id_friend)

    def accept(self,id_user,id_friend):
        cur = None
        conn = None

        try:
            conn = self.db.getConnection()
            cur = conn.cursor()
            cur.execute("UPDATE youshare.friendships SET state=%s WHERE id_receiver = %s AND id_asker = %s"
                        , [enum.STATE_ACCEPTED, id_user, id_friend])

        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()

    def refuseFriendRequest(self,id_user,id_friend):
        if id_user == id_friend:
            raise falcon.HTTPForbidden("Forbidden", "You cannot refuse yourself as a friend")
        if not self.userServices.userExist(id_friend):
            raise falcon.HTTPNotFound("Not Found", "User not found")
        if not self.friendRequestExist(id_user, id_friend):
            raise falcon.HTTPNotFound("Not Found", "Friend request don't exist")
        cur = None
        conn = None

        try:
            conn = self.db.getConnection()
            cur = conn.cursor()

            cur.execute("SELECT state FROM youshare.friendships WHERE id_receiver = %s AND id_asker = %s",
                        [id_user, id_friend])
            state = cur.fetchone()
        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err

        conn.commit()
        cur.close()
        self.db.freeConnexion()

        if state is None:
            raise falcon.HTTPForbidden("Forbidden", "You cannot refuse a friend request when you are the asker")
        elif state[0] == enum.STATE_REFUSED:
            raise falcon.HTTPConflict("Conflict", "Friend request already refused")
        elif state[0] == enum.STATE_ACCEPTED:
            raise falcon.HTTPForbidden("Forbidden", "You cannot refuse a friend already accepted")
        else:
            self.refuse(id_friend,id_user)



    def refuse(self,id_friend,id_user):

        cur = None
        conn = None
        try:
            conn = self.db.getConnection()
            cur = conn.cursor()
            cur.execute("UPDATE youshare.friendships SET state=%s WHERE id_receiver = %s AND id_asker = %s"
                        , [enum.STATE_REFUSED, id_user, id_friend])
        except BaseException as err:
            conn.rollback()
            logger.warning(err)
            raise err
