import bcrypt
import falcon
from src.data.db import Db
from src.utils import enum
from src.models.users import Users


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
            self.db = Db.getInstance()

    def getUsersLike(self,username):
        conn = self.db.getConnection()
        cur = conn.cursor()
        cur.execute("SELECT id_user, username, role, email, biography,picture FROM youshare.users WHERE username LIKE %s",["%"+username+"%"])
        data = cur.fetchall()


        users = []

        for user in data:
            users.append(Users.from_tuple(user).__dict__)

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        if len(users) == 0:
            raise falcon.HTTPNotFound('Not found','No users found')

        return users

    def getUser(self, idUser):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute("SELECT id_user, username, role, email, biography,picture FROM youshare.users WHERE id_user=%s", [idUser])
        data = cur.fetchone()

        if data is None:
            self.conn.commit
            cur.close()
            raise falcon.HTTPNotFound('Not Found', 'The user is not found')

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        user = Users.from_tuple(data)

        return user

    def userExist(self,id_user):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute("SELECT id_user, username, role, email, biography FROM youshare.users WHERE id_user=%s",
                    [id_user])

        user = cur.fetchone()

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return user is not None

    def usernameExist(self,username):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id_user, username, role, email, biography FROM youshare.users WHERE lower(username)=lower(%s)",
            [username])

        user = cur.fetchone()

        conn.commit()
        cur.close()
        self.db.freeConnexion()

        return user is not None

    def emailExist(self, email):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id_user, username, role, email, biography FROM youshare.users WHERE lower(email) = lower(%s)",
            [email])

        user = cur.fetchone()

        conn.commit()
        cur.close()
        return user is not None

    def emailAndIdDifferentExist(self, email, id_user):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id_user, username, role, email, biography FROM youshare.users WHERE lower(email) = lower(%s) and id_user!=%s",
            [email, id_user])

        user = cur.fetchone()

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return user is not None

    def usernameAndIdDifferentExist(self, username, id_user):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id_user, username, role, email, biography FROM youshare.users WHERE lower(username)=lower(%s) AND id_user != %s",
            [username, id_user])

        user = cur.fetchone()

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return user is not None

    def grantAdmin(self, id_user):
        # Verify if user exist and send 404 if not
        user = self.getUser(id_user)

        if user.role == enum.ROLE_ADMIN:
            raise falcon.HTTPBadRequest("Bad Request", "User is already an admin")

        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute("UPDATE youshare.users SET role = %s WHERE id_user = %s "
                    "RETURNING id_user, username, role, email, biography,picture", [enum.ROLE_ADMIN, id_user])

        data = cur.fetchone()

        conn.commit()
        cur.close()
        self.db.freeConnexion()

        user = Users.from_tuple(data)

        return user

    def verifyPassword(self,id_user,password):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute("SELECT password FROM youshare.users WHERE id_user = %s",
                    [id_user])

        user = cur.fetchone()

        password = str(password).encode('utf-8')
        hashedPassword = str(user[0]).encode('utf-8')

        conn.commit()
        cur.close()
        self.db.freeConnexion()
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

        sql += " WHERE id_user = %s RETURNING id_user, username, role, email, biography,picture "
        params.append(body['id_user'])

        conn = self.db.getConnection()
        cur = conn.cursor()
        cur.execute(sql, params)
        data = cur.fetchone()

        conn.commit()
        cur.close()
        self.db.freeConnexion()

        user = Users.from_tuple(data)

        return user

    def registerUser(self, email, username, password: str):
        conn = self.db.getConnection()
        cur = conn.cursor()

        if self.emailExist(email):
            conn.commit()
            cur.close()
            raise falcon.HTTPConflict('Conflict', 'The email address is already used')

        if self.usernameExist(username):
            conn.commit()
            cur.close()
            raise falcon.HTTPConflict('Conflict', 'The username is already used')

        password = str(password).encode('utf-8');
        hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt(10))
        hashedPassword = hashedPassword.decode('utf-8')
        cur.execute("INSERT INTO youshare.users(email,username,password)"
                    " VALUES (%s,%s,%s) RETURNING id_user",
                    [email, username, hashedPassword])
        row = cur.fetchone()

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return row[0]

    def login(self, username, password):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute("SELECT id_user,password FROM youshare.users WHERE lower(username) = lower(%s)",
                    [username])
        user = cur.fetchone()

        if user is None:
            self.conn.commit()
            cur.close()
            raise falcon.HTTPNotFound('Not Found', 'The user is not registered yet')

        password = str(password).encode('utf-8')
        hashedPassword = str(user[1]).encode('utf-8')

        if not bcrypt.checkpw(password, hashedPassword):
            raise falcon.HTTPUnauthorized("Unauthorized", "the password is incorrect")

        conn.commit()
        cur.close()
        self.db.freeConnexion()
        return user[0]

    def getPicture(self, id_user):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute("SELECT picture FROM youshare.users WHERE id_user = %s",
                    [id_user])
        picture_name = cur.fetchone()
        if picture_name is None or picture_name[0] is None:
            raise falcon.HTTPNotFound('Not Found', 'The user has no picture')
        conn.commit()
        cur.close()
        self.db.freeConnexion()

        return picture_name[0]

    def updateUserPicture(self, id_user, picture):
        conn = self.db.getConnection()
        cur = conn.cursor()

        cur.execute("UPDATE youshare.users SET picture = %s WHERE id_user = %s",
                    [picture, id_user])
        #TODO eliott peut être checker des erreurs ?
        conn.commit()
        cur.close()
        self.db.freeConnexion()



