import html
from src.utils.pictureManager import convert_picture

class Friends:

    def __init__(self,status:str, id_user: int, username: str, role: str,
                 email: str, biography: str = None, picture: str = None):
        self.id_user = id_user
        self.username = username
        self.role = role
        self.email = email
        self.biography = biography
        self.picture = picture
        self.status = status

    @classmethod
    def from_tuple(cls, tuple):
        temp = (tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], convert_picture(tuple[6]))
        return cls(*temp)

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
        if self.status is not None:
            self.status = html.unescape(self.status)
        return self