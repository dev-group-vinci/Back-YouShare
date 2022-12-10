import bcrypt
import falcon
from src.data.db import Db
from src.utils import enum


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
            db = Db.getInstance()
            self.conn = db.conn


    def getAll(self,id_user):

        cur = self.conn.cursor()


        cur.execute(
            "SELECT us.id_user,us.username,us.email,us.biography,us.role "
            "FROM youshare.friendships as fr, youshare.users as us "
            "WHERE CASE WHEN fr.id_asker = %s THEN us.id_user = id_receiver ELSE us.id_user = id_asker END "
            "AND (fr.id_asker = %s OR fr.id_receiver = %s) "
            "AND fr.state = 'accepted' ",
            (id_user, id_user, id_user)
        )

        # Récupérez les résultats de la requête
        friends = cur.fetchall()

        list = []

        # Affichez les amis de l'utilisateur et leur rôle (expéditeur ou destinataire)
        for friend in friends:
            user = {
                "id_user":friend[0],
                "username":friend[1],
                "role": friend[4],
                "email": friend[2],
                "biography":friend[3]
            }
            list.append(user)

        self.conn.commit()
        cur.close()
        return list


