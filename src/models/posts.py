class Post:

    def __init__(self, id_post, id_user, id_url,
                 state, date_published
                 , date_deleted, text):
        self.id_post = id_post
        self.id_user = id_user
        self.id_url = id_url
        self.state = state
        self.date_published = date_published
        self.date_deleted = date_deleted
        self.text = text

    @classmethod
    def from_tuple(cls, tuple):
        return cls(*tuple)

