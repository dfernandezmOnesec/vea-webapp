import os
from datetime import datetime, timedelta
from azure.storage.blob import (
    BlobServiceClient, generate_blob_sas, generate_container_sas,
    ContentSettings
)

# Conexión base
def get_blob_service_client():
    account_name = os.environ['BLOB_ACCOUNT_NAME']
    account_key = os.environ['BLOB_ACCOUNT_KEY']
    connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    return BlobServiceClient.from_connection_string(connect_str)

# Subida de archivo
def upload_file(bytes_data, file_name, content_type='application/pdf'):
    container_name = os.environ['BLOB_CONTAINER_NAME']
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    
    blob_client.upload_blob(bytes_data, overwrite=True, content_settings=ContentSettings(content_type=content_type))

    sas_token = generate_blob_sas(
        account_name=os.environ['BLOB_ACCOUNT_NAME'],
        container_name=container_name,
        blob_name=file_name,
        account_key=os.environ['BLOB_ACCOUNT_KEY'],
        permission="r",
        expiry=datetime.utcnow() + timedelta(hours=3)
    )
    
    return f"{blob_client.url}?{sas_token}"

# Obtención de todos los archivos
def get_all_files():
    account_name = os.environ['BLOB_ACCOUNT_NAME']
    account_key = os.environ['BLOB_ACCOUNT_KEY']
    container_name = os.environ['BLOB_CONTAINER_NAME']
    
    blob_service_client = get_blob_service_client()
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs(include='metadata')
    
    sas = generate_container_sas(
        account_name, container_name,
        account_key=account_key,
        permission="r",
        expiry=datetime.utcnow() + timedelta(hours=3)
    )

    files = []
    converted_files = {}

    for blob in blob_list:
        if not blob.name.startswith('converted/'):
            files.append({
                "filename": blob.name,
                "converted": blob.metadata.get('converted', 'false') == 'true' if blob.metadata else False,
                "embeddings_added": blob.metadata.get('embeddings_added', 'false') == 'true' if blob.metadata else False,
                "fullpath": f"https://{account_name}.blob.core.windows.net/{container_name}/{blob.name}?{sas}",
                "converted_path": ""
            })
        else:
            converted_files[blob.name] = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob.name}?{sas}"

    for file in files:
        converted_filename = f"converted/{file['filename']}.zip"
        if converted_filename in converted_files:
            file['converted'] = True
            file['converted_path'] = converted_files[converted_filename]

    return files

# Agregar o actualizar metadatos
def upsert_blob_metadata(file_name, metadata):
    container_name = os.environ['BLOB_CONTAINER_NAME']
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    blob_metadata = blob_client.get_blob_properties().metadata
    blob_metadata.update(metadata)
    blob_client.set_blob_metadata(metadata=blob_metadata)
