import bcrypt
import falcon
from src.data.db import Db


class UserService:
    __instance = None

    @staticmethod
    def getInstance():
        if UserService.__instance is None:
            UserService()
        return UserService.__instance
    def __init__(self):
        if UserService.__instance is not None:
            raise Exception("UserService instance already exist !!")
        else:
            UserService.__instance = self
        db = Db.getInstance()
        self.conn = db.conn


    def getUser(self, idUser):
        return {
            "id": idUser,
            "username": "mehdi"
        }

    def registerUser(self, email, username, password: str):
        cur = self.conn.cursor()

        cur.execute("SELECT * FROM youshare.users WHERE email=%s", [email])
        data = cur.fetchone()
        if data is not None:
            self.conn.commit()
            cur.close()
            raise falcon.HTTPConflict('Conflict', 'The user is already registered')

        password = str(password).encode('utf-8');
        hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt(10))
        hashedPassword = hashedPassword.decode('utf-8')
        cur.execute("INSERT INTO youshare.users(email,username,password)"
                    " VALUES (%s,%s,%s) RETURNING id_user,username",
                    [email, username, hashedPassword])
        row = cur.fetchone()

        self.conn.commit()
        cur.close()
        return row[0]

    def login(self, email, password):
        cur = self.conn.cursor()

        cur.execute("SELECT id_user,username,role,password FROM youshare.users WHERE email = %s", [email])
        user = cur.fetchone()
        if user is None:
            self.conn.commit()
            cur.close()
            raise falcon.HTTPNotFound('Not Found', 'The user is not registered yet')
        password = str(password).encode('utf-8')
        hashedPassword = str(user[3]).encode('utf-8')
        if not bcrypt.checkpw(password, hashedPassword):
            raise falcon.HTTPUnauthorized("Unauthorized", "the password is incorrect")

        self.conn.commit()
        cur.close()

        return user[0]
