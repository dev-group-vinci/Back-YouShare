import os
import falcon
from src.data.db import Db
from src.middleware import logging
from src.utils.logging import logger
from wsgiref.simple_server import make_server
from src.resources.PostResource import Posts
from src.resources.LikeResource import Likes
from src.resources.ShareResource import Shares
from src.resources.FriendsResource import Friends
from src.resources.CommentsResource import Comments
from src.resources.UserResource import UserRessource

if __name__ == '__main__':
    api = falcon.App(cors_enable=False, middleware=[
        logging.LoggingMiddleware()
    ])

    # database connection
    database = Db().getInstance()
    database.connect()

    users = UserRessource()
    posts = Posts()
    likes = Likes()
    shares = Shares()
    friends = Friends()
    comments = Comments()

    api.add_route('/friends',friends)
    api.add_route('/friends/requests',friends,suffix='requests')
    api.add_route('/friends/self/requests',friends,suffix='self')
    api.add_route('/friends/{id_friend}',friends,suffix='id')
    api.add_route('/friends/{id_friend}/accept',friends,suffix='accept')
    api.add_route('/friends/{id_friend}/refuse', friends, suffix='refuse')

    api.add_route('/users',users)
    api.add_route('/users/{id_user}',users,suffix='id')
    api.add_route('/users/login', users, suffix='login')
    api.add_route('/users/register', users, suffix='register')
    api.add_route('/users/{id_user}/picture', users, suffix='picture')
    api.add_route('/users/self/picture', users, suffix='self_picture')
    api.add_route('/users/search/{username}',users,suffix='search')

    api.add_route('/posts', posts)
    api.add_route('/posts/me', posts, suffix='me')
    api.add_route('/posts/{id_post}', posts, suffix='post')

    api.add_route('/posts/{id_post}/likes', likes)
    api.add_route('/posts/{id_post}/likes/is_liked', likes, suffix='liked')
    api.add_route('/posts/{id_post}/shares', shares)
    api.add_route('/posts/{id_post}/shares/is_shared', shares, suffix='shared')

    api.add_route('/posts/{id_post}/comments/', comments)
    api.add_route('/posts/comments/', comments)
    api.add_route('/posts/comments/{id_comment}', comments, suffix='id')
    api.add_route('/posts/{id_post}/comments/{id_comment}', comments, suffix='one')

    logger.info("Server started")

    port = int(os.getenv("PORT")) or 8080

    with make_server('', port, api) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        logger.info("Server closed")
        database.freeConnexion()
        httpd.server_close()
