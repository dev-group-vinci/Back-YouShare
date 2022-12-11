class Like:
    def __init__(self, id_user, id_post):
        self.id_user = id_user
        self.id_post = id_post

    @classmethod
    def from_tuple(cls, tuple):
        return cls(*tuple)
