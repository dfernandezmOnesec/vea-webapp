from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contact
from utilities.azureblobstorage import upload_to_blob
import json
import os
import io
import zipfile

@receiver(post_save, sender=Contact)
def upload_contact_to_blob(sender, instance, created, **kwargs):
    data = {
        "id": instance.id,
        "name": getattr(instance, 'name', None),
        "email": getattr(instance, 'email', None),
        # ...otros campos relevantes
    }
    json_blob_name = f"contact_{instance.id}.json"
    # Guardar JSON temporalmente
    with open(json_blob_name, "w", encoding="utf-8") as f:
        json.dump(data, f)
    # Subir JSON a la raíz
    upload_to_blob(json_blob_name, json_blob_name)
    # Crear ZIP en memoria con el JSON
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        with open(json_blob_name, 'rb') as f:
            zip_file.writestr(json_blob_name, f.read())
    buffer.seek(0)
    zip_blob_name = f"converted/{json_blob_name}.zip"
    upload_to_blob(buffer, zip_blob_name)
    os.remove(json_blob_name) 