class Comment:

    def __init__(self, id_comment=None, id_user=None, id_post=None,
                 id_comment_parent=None, text=None, state=None,
                 date_published=None, date_deleted=None):
        self.id_comment = id_comment
        self.id_user = id_user
        self.id_post = id_post
        self.id_comment_parent = id_comment_parent
        self.text = text
        self.state = state
        self.date_published = date_published
        self.date_deleted = date_deleted

    @classmethod
    def from_tuple(cls, tuple):
        return cls(*tuple)

    def create_new_comment_from_json(self, json):
        self.id_post = json['id_post']
        if 'id_comment_parent' in json:
            self.id_comment_parent = json['id_comment_parent']
        self.text = json['text']
        return self
