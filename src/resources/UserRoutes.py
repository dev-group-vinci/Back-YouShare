
import os
from datetime import datetime, timedelta
import base64

import falcon
from json import dumps

from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from falcon.media.validators import jsonschema
from src.media import load_schema
from src.utils.Authenticate import Authenticate
from src.services.UsersService import UserService
from src.utils import enum

auth = Authenticate()

class Users:
    def __init__(self):
        self.userServices = UserService.getInstance()

    @falcon.before(auth,enum.ROLE_USER)
    def on_get(self,req,resp):
        resp.status = falcon.HTTP_200
        resp.body = dumps(req.context.user)

    @jsonschema.validate(load_schema('user_login'))
    def on_post_login(self, req, resp):
        raw_json = req.media
        id = self.userServices.login(raw_json['username'],raw_json['password'])
        token = auth.encode(id_user=int(id))
        resp.status = falcon.HTTP_200
        resp.body = dumps({
            'token': token
        })

    @jsonschema.validate(load_schema('user_register'))
    def on_post_register(self, req, resp):
        # récupérer le json
        raw_json = req.media
        resp.status = falcon.HTTP_200
        id = self.userServices.registerUser(raw_json['email'], raw_json['username'], raw_json['password'])

        token = auth.encode(id_user=int(id))
        # renvoyer le json
        resp.body = dumps(token)


    def on_get_picture(self, req, resp, picture_name):
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

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=picture_name)
        url = blob_client.url + "?" + sas_token


        resp.status = falcon.HTTP_200
        resp.body = dumps({'url': url})

    def on_post_picture(self, req, resp, picture_name): #TODO savoir quoi mettre dans le body (surment picture_name)
        # récupérer le json
        raw_json = req.media

        now = datetime.now()
        nameSaved = 'helloworld' + now.strftime("%d-%m-%Y-%H:%M:%S") + '.png'

        connection_string = os.getenv("CONNECTION_STRING")
        container_name = os.getenv("CONTAINER_NAME")

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=nameSaved)

        with open("./helloworld.png", "rb") as data: #TODO hardcode le path du fichier
            blob_client.upload_blob(data)
            print(f"Uploaded {nameSaved}.") # TODO enlever le print ?

        resp.status = falcon.HTTP_200
        # renvoyer le json
        resp.body = dumps(raw_json)
