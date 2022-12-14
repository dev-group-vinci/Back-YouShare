import html

class Users:

    def __init__(self, id_user: int, username: str, role: str,
                 email: str, biography: str = None, picture: str = None):
        self.id_user = id_user
        self.username = username
        self.role = role
        self.email = email
        self.biography = biography
        self.picture = picture

    @classmethod
    def from_tuple(cls, tuple):
        return cls(*tuple)

    @staticmethod
    def new_user_from_json(self, json):
        self.username = json['username']
        self.email = json['email']
        self.password = json['password']
        return self

    def unescape(self):
        if self.username is not None:
            self.username = html.unescape(self.username)
        if self.role is not None:
            self.role = html.unescape(self.role)
        if self.email is not None:
            self.email = html.unescape(self.email)
        if self.biography is not None:
            self.biography = html.unescape(self.biography)
        if self.picture is not None:
            self.picture = html.unescape(self.picture)
        return self

