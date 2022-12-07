class UserService:
    def __init__(self, conn):
        self.conn = conn

    def getUser(self, idUser):
        return {
            "id": idUser,
            "username": "mehdi"
        }

    def registerUser(self, email, username, password):
        pass

    def loginUser(self, email, password):
        pass
