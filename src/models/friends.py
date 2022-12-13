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
        return cls(*tuple)