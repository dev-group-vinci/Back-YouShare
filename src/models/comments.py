class Comment:

    def __init__(self, id_comment, id_user, id_post,
                 id_comment_parent, text, state,
                 date_published, date_deleted):
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
