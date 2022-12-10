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
        cur = self.conn.cursor()
        cur.execute("SELECT id_user, username, role, email, biography FROM youshare.users WHERE id_user=%s", [idUser])
        user = cur.fetchone()
        if user is None:
            self.conn.commit
            cur.close()
            raise falcon.HTTPNotFound('Not Found', 'The user is not found')
        self.conn.commit()
        cur.close()

        return {
            "id_user": user[0],
            "username": user[1],
            "role": user[2],
            "email": user[3],
            "biography": user[4]
        }

    def usernameExist(self,username):
        cur = self.conn.cursor()
        cur.execute("SELECT id_user, username, role, email, biography FROM youshare.users WHERE lower(username)=lower(%s)", [username])
        user = cur.fetchone()
        self.conn.commit()
        cur.close()

        return user is not None

    def emailExist(self,email):
        cur = self.conn.cursor()
        cur.execute("SELECT id_user, username, role, email, biography FROM youshare.users WHERE lower(email) = lower(%s)", [email])
        user = cur.fetchone()
        self.conn.commit()
        cur.close()

        return user is not None

    def updateUser(self, body):
        cur = self.conn.cursor()

        # On construit la requête SQL en fonction des champs optionnels fournis
        sql = "UPDATE youshare.users SET"
        params = []
        hasBefore = False
        if 'username' in body:
            if self.usernameExist(body['username']):
                raise falcon.HTTPConflict('Conflict','Username already used')

            if hasBefore:
                sql += ","
            else:
                hasBefore = True

            sql += " username = %s "
            params.append(body['username'])
        if 'email' in body:
            if self.emailExist(body['email']):
                raise falcon.HTTPConflict('Conflict','Email already used')

            if hasBefore:
                sql += ","
            else:
                hasBefore = True

            sql += " email = %s "
            params.append(body['email'])
        if 'biography' in body:

            if hasBefore:
                sql += ","
            else:
                hasBefore = True

            sql += " biography = %s "
            params.append(body['biography'])
        if 'password' in body:

            if hasBefore:
                sql += ","
            else:
                hasBefore = True

            sql += " password = %s "
            password = str(body['password']).encode('utf-8');
            hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt(10))
            hashedPassword = hashedPassword.decode('utf-8')
            params.append(hashedPassword)

        sql += " WHERE id_user = %s RETURNING id_user,username,role,email,biography "
        params.append(body['id_user'])

        cur.execute(sql, params)
        newUser = cur.fetchone()

        self.conn.commit()

        cur.close()



        return {
            "id_user": newUser[0],
            "username": newUser[1],
            "role": newUser[2],
            "email": newUser[3],
            "biography": newUser[4]
        }

    def registerUser(self, email, username, password: str):
        cur = self.conn.cursor()

        if self.emailExist(email) is not None:
            self.conn.commit()
            cur.close()
            raise falcon.HTTPConflict('Conflict', 'The email address is already used')

        if self.usernameExist(username):
            self.conn.commit()
            cur.close()
            raise falcon.HTTPConflict('Conflict', 'The username is already used')

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

    def login(self, username, password):
        cur = self.conn.cursor()

        cur.execute("SELECT id_user,username,role,password FROM youshare.users WHERE lower(username) = lower(%s)", [username])
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
