class Post:

    def __init__(self, id_post=None, id_user=None, id_url=None,
                 state=None, date_published=None,
                 date_deleted=None, text=None):
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

    def create_new_post_from_json(self, json):
        self.id_url = json['id_url']
        self.text = json['text']
        return self
