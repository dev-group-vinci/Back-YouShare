import bcrypt
import falcon
from src.data.db import Db
from src.utils import enum


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

    def userExist(self,id_user):
        cur = self.conn.cursor()
        cur.execute("SELECT id_user, username, role, email, biography FROM youshare.users WHERE id_user=%s",
                    [id_user])
        user = cur.fetchone()
        self.conn.commit()
        cur.close()

        return user is not None

    def usernameExist(self,username):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id_user, username, role, email, biography FROM youshare.users WHERE lower(username)=lower(%s)",
            [username])
        user = cur.fetchone()
        self.conn.commit()
        cur.close()

        return user is not None

    def emailExist(self, email):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id_user, username, role, email, biography FROM youshare.users WHERE lower(email) = lower(%s)",
            [email])
        user = cur.fetchone()
        self.conn.commit()
        cur.close()
        return user is not None

    def emailAndIdDifferentExist(self, email, id_user):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id_user, username, role, email, biography FROM youshare.users WHERE lower(email) = lower(%s) and id_user!=%s",
            [email, id_user])
        user = cur.fetchone()
        self.conn.commit()
        cur.close()
        return user is not None

    def usernameAndIdDifferentExist(self, username, id_user):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id_user, username, role, email, biography FROM youshare.users WHERE lower(username)=lower(%s) AND id_user != %s",
            [username, id_user])
        user = cur.fetchone()
        self.conn.commit()
        cur.close()

        return user is not None

    def grantAdmin(self, id_user):
        # Verify if user exist and send 404 if not
        user = self.getUser(id_user)

        if user['role'] == enum.ROLE_ADMIN:
            raise falcon.HTTPBadRequest("Bad Request", "User is already an admin")

        cur = self.conn.cursor()
        cur.execute("UPDATE youshare.users SET role = %s WHERE id_user = %s "
                    "RETURNING id_user,username,role,email,biography", [enum.ROLE_ADMIN, id_user])
        user = cur.fetchone()
        self.conn.commit()
        cur.close()

        return {
            "id_user": user[0],
            "username": user[1],
            "role": user[2],
            "email": user[3],
            "biography": user[4]
        }

    def verifyPassword(self,id_user,password):

        cur = self.conn.cursor()

        cur.execute("SELECT password FROM youshare.users WHERE id_user = %s",
                    [id_user])
        user = cur.fetchone()
        password = str(password).encode('utf-8')
        hashedPassword = str(user[0]).encode('utf-8')

        self.conn.commit()
        cur.close()
        return bcrypt.checkpw(password, hashedPassword)

    def updateUser(self, body):

        if 'password' not in body:
            raise falcon.HTTPBadRequest('Bad Request', 'Need password to update user')

        elif not self.verifyPassword(body['id_user'], body['password']):
            raise falcon.HTTPUnauthorized('Unauthorized', 'Password incorrect')

        # On construit la requête SQL en fonction des champs optionnels fournis
        sql = "UPDATE youshare.users SET"
        params = []
        hasBefore = False
        if 'username' in body:
            if self.usernameAndIdDifferentExist(body['username'], body['id_user']):
                raise falcon.HTTPConflict('Conflict', 'Username already used')

            if hasBefore:
                sql += ","
            else:
                hasBefore = True

            sql += " username = %s "
            params.append(body['username'])
        if 'email' in body:
            if self.emailAndIdDifferentExist(body['email'], body['id_user']):
                raise falcon.HTTPConflict('Conflict', 'Email already used')

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
        if 'password' in body and 'new_password' in body:

            if hasBefore:
                sql += ","

            sql += " password = %s "
            password = str(body['new_password']).encode('utf-8');
            hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt(10))
            hashedPassword = hashedPassword.decode('utf-8')
            params.append(hashedPassword)

        sql += " WHERE id_user = %s RETURNING id_user,username,role,email,biography "
        params.append(body['id_user'])

        cur = self.conn.cursor()
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

        if self.emailExist(email):
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

        cur.execute("SELECT id_user,username,role,password FROM youshare.users WHERE lower(username) = lower(%s)",
                    [username])
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

    def getPicture(self, id_user):
        cur = self.conn.cursor()

        cur.execute("SELECT picture FROM youshare.users WHERE id_user = %s",
                    [id_user])
        picture_name = cur.fetchone()
        #TODO eliott peut être checker des erreurs ?
        self.conn.commit()
        cur.close()

        return picture_name[0]

    def updateUserPicture(self, id_user, picture):
        cur = self.conn.cursor()

        cur.execute("UPDATE youshare.users SET picture = %s WHERE id_user = %s",
                    [picture, id_user])
        #TODO eliott peut être checker des erreurs ?
        self.conn.commit()
        cur.close()



