import html
import os
from datetime import datetime, timedelta
import uuid
import falcon
from json import dumps
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from falcon.media.validators import jsonschema
from src.media import load_schema
from src.utils.Authenticate import Authenticate
from src.services.UsersService import UserService
from src.utils import enum
from src.utils.json import parseList,parseElement

auth = Authenticate.getInstance()


class UserServices:
    def __init__(self):
        self.userServices = UserService.getInstance()

    @falcon.before(auth, enum.ROLE_USER)
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        resp.body = dumps(parseElement(req.context.user))

    @jsonschema.validate(load_schema('user_update'))
    @falcon.before(auth, enum.ROLE_USER)
    def on_put(self, req, resp):
        raw_json = req.media

        raw_json['id_user'] = req.context.user.id_user

        if 'username' in raw_json:
            raw_json['username'] = html.escape(raw_json['username'])
        if 'biography' in raw_json:
            raw_json['biography'] = html.escape(raw_json['biography'])
        if 'email' in raw_json:
            raw_json['email'] = html.escape(raw_json['email'])

        userUpdated = self.userServices.updateUser(raw_json).unescape()

        resp.status = falcon.HTTP_200
        resp.body = dumps(parseElement(userUpdated))

    @falcon.before(auth, enum.ROLE_USER)
    def on_get_id(self, req, resp, id_user):
        user = self.userServices.getUser(id_user).unescape()
        resp.status = falcon.HTTP_200
        resp.body = dumps(parseElement(user))

    @falcon.before(auth, enum.ROLE_ADMIN)
    def on_put_id(self, req, resp, id_user):
        user = self.userServices.grantAdmin(id_user).unescape()
        resp.status = falcon.HTTP_200
        resp.body = dumps(parseElement(user))

    @falcon.before(auth, enum.ROLE_USER)
    def on_get_search(self, req, resp, username):
        users = self.userServices.getUsersLike(html.escape(username))
        resp.status = falcon.HTTP_200
        resp.body = dumps(parseList(users))

    @jsonschema.validate(load_schema('user_login'))
    def on_post_login(self, req, resp):
        raw_json = req.media
        id = self.userServices.login(html.escape(raw_json['username']), raw_json['password'])
        token = auth.encode(id_user=int(id))
        resp.status = falcon.HTTP_200
        resp.body = dumps({
            'token': token
        })

    @jsonschema.validate(load_schema('user_register'))
    def on_post_register(self, req, resp):
        # récupérer le json
        raw_json = req.media

        id = self.userServices.registerUser(html.escape(raw_json['email']),
                                            html.escape(raw_json['username']),
                                            html.escape(raw_json['password']))

        token = auth.encode(id_user=int(id))

        resp.status = falcon.HTTP_201
        resp.body = dumps({
            'token': token
        })

    @falcon.before(auth, enum.ROLE_USER)
    def on_get_picture(self, req, resp, id_user):
        # get picture name from db
        picture_name = self.userServices.getPicture(id_user)

        connection_string = os.getenv("CONNECTION_STRING")
        container_name = os.getenv("CONTAINER_NAME")

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Create a SAS token to use to authenticate a new client
        sas_token = generate_account_sas(
            blob_service_client.account_name,
            account_key=blob_service_client.credential.account_key,
            resource_types=ResourceTypes(object=True),
            permission=AccountSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )

        # get image from azure blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=picture_name)
        url = blob_client.url + "?" + sas_token

        resp.status = falcon.HTTP_200
        resp.body = dumps({'url': url})

    @falcon.before(auth, enum.ROLE_USER)
    def on_get_self_picture(self, req, resp):
        # get picture name from db
        picture_name = self.userServices.getPicture(req.context.user.id_user)

        connection_string = os.getenv("CONNECTION_STRING")
        container_name = os.getenv("CONTAINER_NAME")

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Create a SAS token to use to authenticate a new client
        sas_token = generate_account_sas(
            blob_service_client.account_name,
            account_key=blob_service_client.credential.account_key,
            resource_types=ResourceTypes(object=True),
            permission=AccountSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )

        # get image from azure blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=picture_name)
        url = blob_client.url + "?" + sas_token

        resp.status = falcon.HTTP_200
        resp.body = dumps({'url': url})

    @falcon.before(auth, enum.ROLE_USER)
    def on_post_self_picture(self, req, resp):
        form = req.get_media()
        for part in form:
            if part.name == 'image':
                # Create a unique name
                now = datetime.now()
                name_saved = now.strftime("%d-%m-%Y-%H:%M:%S") + str(uuid.uuid4()) + "." + \
                             part.secure_filename.rsplit('.', 1)[1]

                # Send to Azure blob storage
                connection_string = os.getenv("CONNECTION_STRING")
                container_name = os.getenv("CONTAINER_NAME")

                blob_service_client = BlobServiceClient.from_connection_string(connection_string)
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=name_saved)

                blob_client.upload_blob(part.stream)

                # Insert into database
                self.userServices.updateUserPicture(req.context.user.id_user, name_saved)

                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
