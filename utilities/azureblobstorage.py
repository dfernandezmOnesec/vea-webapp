import os
from datetime import datetime, timedelta
from azure.storage.blob import (
    BlobServiceClient, generate_blob_sas, generate_container_sas,
    ContentSettings
)
from django.conf import settings
import requests

# Conexión base
def get_blob_service_client():
    """Obtiene el cliente de servicio de Azure Blob Storage."""
    try:
        account_name = settings.BLOB_ACCOUNT_NAME
        account_key = settings.BLOB_ACCOUNT_KEY
        if not account_name or not account_key:
            raise ValueError("BLOB_ACCOUNT_NAME y BLOB_ACCOUNT_KEY son requeridos")
        
        connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        return BlobServiceClient.from_connection_string(connect_str)
    except Exception as e:
        print(f"Error al crear el cliente de Blob Storage: {str(e)}")
        raise

# Subida de archivo
def upload_file(bytes_data, file_name, content_type='application/pdf'):
    """Sube un archivo a Azure Blob Storage."""
    try:
        container_name = settings.BLOB_CONTAINER_NAME
        if not container_name:
            raise ValueError("BLOB_CONTAINER_NAME es requerido")

        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
        
        blob_client.upload_blob(bytes_data, overwrite=True, content_settings=ContentSettings(content_type=content_type))

        sas_token = generate_blob_sas(
            account_name=settings.BLOB_ACCOUNT_NAME,
            container_name=container_name,
            blob_name=file_name,
            account_key=settings.BLOB_ACCOUNT_KEY,
            permission="r",
            expiry=datetime.utcnow() + timedelta(hours=3)
        )
        
        return f"{blob_client.url}?{sas_token}"
    except Exception as e:
        print(f"Error al subir el archivo {file_name}: {str(e)}")
        raise

# Obtención de todos los archivos
def get_all_files():
    """Obtiene todos los archivos del contenedor."""
    try:
        account_name = settings.BLOB_ACCOUNT_NAME
        account_key = settings.BLOB_ACCOUNT_KEY
        container_name = settings.BLOB_CONTAINER_NAME
        
        if not all([account_name, account_key, container_name]):
            raise ValueError("Configuración incompleta de Azure Blob Storage")
        
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
    except Exception as e:
        print(f"Error al obtener archivos: {str(e)}")
        raise

# Agregar o actualizar metadatos
def upsert_blob_metadata(file_name, metadata):
    """Actualiza los metadatos de un blob."""
    try:
        container_name = settings.BLOB_CONTAINER_NAME
        if not container_name:
            raise ValueError("BLOB_CONTAINER_NAME es requerido")
            
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        blob_metadata = blob_client.get_blob_properties().metadata
        blob_metadata.update(metadata)
        blob_client.set_blob_metadata(metadata=blob_metadata)
    except Exception as e:
        print(f"Error al actualizar metadatos de {file_name}: {str(e)}")
        raise

def upload_to_blob(file_or_buffer, blob_name):
    """
    Sube un archivo a Azure Blob Storage.
    file_or_buffer puede ser una ruta (str/Path) o un buffer (BytesIO).
    """
    try:
        # Verificar si los signals de Azure están deshabilitados
        if getattr(settings, 'DISABLE_AZURE_SIGNALS', False):
            print(f"Azure signals deshabilitados. Omitiendo subida de {blob_name}")
            return None

        print(f"Intentando subir {blob_name} a Azure Blob Storage...")

        if not blob_name:
            raise ValueError("blob_name es requerido")

        if not all([settings.BLOB_ACCOUNT_NAME, settings.BLOB_ACCOUNT_KEY, settings.BLOB_CONTAINER_NAME]):
            raise ValueError("Configuración incompleta de Azure Blob Storage")

        print(f"Cuenta: {settings.BLOB_ACCOUNT_NAME}, Contenedor: {settings.BLOB_CONTAINER_NAME}")

        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=settings.BLOB_CONTAINER_NAME,
            blob=blob_name
        )

        # Si es ruta, abrir el archivo; si es buffer, usarlo directamente
        if isinstance(file_or_buffer, (str, bytes, os.PathLike)):
            with open(file_or_buffer, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
        else:
            # Asumimos que es un buffer tipo BytesIO
            file_or_buffer.seek(0)
            blob_client.upload_blob(file_or_buffer, overwrite=True)

        print("Subida exitosa.")
        return blob_client.url

    except Exception as e:
        print(f"Error en upload_to_blob: {str(e)}")
        raise

def trigger_document_processing(blob_name):
    """
    Llama a la Azure Function con un HTTP Trigger para iniciar el procesamiento.
    """
    try:
        function_url = settings.FUNCTION_APP_URL
        function_key = settings.FUNCTION_APP_KEY

        if not function_url or not function_key:
            print("Advertencia: FUNCTION_APP_URL o FUNCTION_APP_KEY no están configuradas. Omitiendo trigger.")
            return None

        headers = {
            'Content-Type': 'application/json',
            'x-functions-key': function_key
        }
        
        # El cuerpo del payload puede ajustarse a lo que tu Azure Function espere.
        # Por ejemplo, el nombre del blob que debe procesar.
        payload = {
            'blob_name': blob_name
        }

        print(f"Llamando a Azure Function para procesar: {blob_name}")
        
        response = requests.post(function_url, headers=headers, json=payload, timeout=30)
        
        response.raise_for_status()  # Lanza una excepción para respuestas 4xx/5xx

        print(f"Llamada a Azure Function exitosa. Status: {response.status_code}")
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error al llamar a la Azure Function: {str(e)}")
        # Aquí podrías reintentar o registrar el fallo para un procesamiento posterior
        return None
    except Exception as e:
        print(f"Error inesperado al disparar la función: {str(e)}")
        return None
