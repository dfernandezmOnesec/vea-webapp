from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Document
from utilities.azureblobstorage import upload_to_blob
import json
import os
import io
import zipfile

@receiver(post_save, sender=Document)
def upload_document_to_blob(sender, instance, created, **kwargs):
    # Verificar si los signals de Azure están deshabilitados
    try:
        if getattr(settings, 'DISABLE_AZURE_SIGNALS', False):
            return
    except:
        # Si no se puede acceder a settings, asumir que está deshabilitado
        return
    
    print(f"Señal post_save activada para Document: {instance.id}")
    # Subir el archivo si existe
    if instance.file:
        file_path = instance.file.path
        blob_name = os.path.basename(file_path)
        print(f"Llamando a upload_to_blob para archivo: {file_path}")
        url = upload_to_blob(file_path, blob_name)
        print(f"Archivo subido a Azure Blob Storage: {url}")
        # Opcional: guardar la URL en el modelo si tienes un campo azure_url
        # instance.azure_url = url
        # instance.save(update_fields=['azure_url'])

        # Crear ZIP en memoria con el archivo original y metadata.json
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zip_file:
            # Agregar el archivo original
            with open(file_path, 'rb') as f:
                zip_file.writestr(blob_name, f.read())
            # Agregar metadatos
            metadata = {
                "id": instance.id,
                "title": instance.title,
                "description": instance.description,
                # Puedes agregar más campos aquí
                "file": instance.file.name if instance.file else None,
            }
            zip_file.writestr('metadata.json', json.dumps(metadata, ensure_ascii=False, indent=2))
        buffer.seek(0)
        zip_blob_name = f"converted/{blob_name}.zip"
        print(f"Llamando a upload_to_blob para ZIP: {zip_blob_name}")
        upload_to_blob(buffer, zip_blob_name)
        print(f"ZIP subido a Azure Blob Storage: {zip_blob_name}") 