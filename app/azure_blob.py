from flask import current_app
from datetime import datetime, timedelta
from azure.storage.blob import generate_container_sas, ContainerSasPermissions, generate_blob_sas, BlobSasPermissions, \
    ContentSettings, ContainerClient


# save image to blob
def save_image(blob_name, file_path):
    container_client = ContainerClient.from_connection_string(
        conn_str=current_app.config['AZURE_STORAGE_CONNECTION_STRING'],
        container_name=current_app.config['AZURE_STORAGE_CONTAINER_NAME'])
    with open(file_path, "rb") as data:
        container_blob = container_client.upload_blob(name=blob_name, data=data,
                                                      overwrite=True)
    return container_blob


# using generate_container_sas
def get_img_url_with_container_sas_token(blob_name):
    account_name = current_app.config['AZURE_STORAGE_ACCOUNT_NAME']
    account_key = current_app.config['AZURE_STORAGE_ACCOUNT_KEY']
    container_name = current_app.config['AZURE_STORAGE_CONTAINER_NAME']
    container_sas_token = generate_container_sas(
        account_name=account_name,
        container_name=container_name,
        account_key=account_key,
        permission=ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url_with_container_sas_token = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?" \
                                        f"{container_sas_token}"
    return blob_url_with_container_sas_token


# using generate_blob_sas
def get_img_url_with_blob_sas_token(blob_name):
    account_name = current_app.config['AZURE_STORAGE_ACCOUNT_NAME']
    account_key = current_app.config['AZURE_STORAGE_ACCOUNT_KEY']
    container_name = current_app.config['AZURE_STORAGE_CONTAINER_NAME']
    blob_sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url_with_blob_sas_token = f"https://{account_name}.blob.core.windows.net/{container_name}/" \
                                   f"{blob_name}?{blob_sas_token}"
    return blob_url_with_blob_sas_token
