import os
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from datetime import datetime, timedelta


def convert_picture(picture_name):
    if picture_name is None:
        return None

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
    return blob_client.url + "?" + sas_token
