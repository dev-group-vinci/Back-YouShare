import os
from datetime import datetime, timedelta

import falcon
from json import dumps

from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from falcon.media.validators import jsonschema
from src.media import load_schema


class Users:
    def on_get_email(self, req, resp):
        resp.status = falcon.HTTP_200
        if req.params:
            resp.media = req.params['id']
        else:
            resp.media = {'Message': 'Hello my friend'}

    def on_get_name(self, req, resp, name):
        resp.status = falcon.HTTP_200
        resp.media = {'Message': 'Hello World ' + name}

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

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {'Message': 'Hello World '}

    @jsonschema.validate(load_schema('user_schema'))
    def on_post(self, req, resp):
        # récupérer le json
        raw_json = req.media

        resp.status = falcon.HTTP_200
        # renvoyer le json
        resp.body = dumps(raw_json)

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
