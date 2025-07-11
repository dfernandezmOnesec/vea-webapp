# apps/documents/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from .models import Document
import mimetypes
import datetime
from django.http import HttpResponseRedirect, FileResponse, Http404, HttpResponse
from django.db import models
from utilities.azureblobstorage import upload_to_blob, trigger_document_processing
from django.conf import settings
import logging
import requests

logger = logging.getLogger(__name__)

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            if not document.date:
                document.date = datetime.datetime.now()
            # Obtener la extensión del archivo
            file_name = request.FILES['file'].name
            file_extension = file_name.split('.')[-1].lower()
            document.file_type = file_extension
            document.is_processed = False
            
            # Subir el archivo a Azure Blob Storage
            file = request.FILES['file']
            blob_name = file.name
            
            try:
                url = upload_to_blob(file, file.name)  # Subir solo con el nombre
                if url:
                    document.file.name = file.name  # Guardar solo el nombre
                    document.save()
                    # Disparar la Azure Function para el procesamiento
                    trigger_document_processing(file.name)
                    messages.success(request, f"El documento '{document.title}' se subió correctamente.")
                    return redirect('documents:document_list')
                else:
                    form.add_error(None, "No se pudo subir el archivo a Azure.")
            except Exception as e:
                form.add_error(None, f"Error al procesar el documento: {e}")
    else:
        form = DocumentForm()
    return render(request, 'documents/create.html', {'form': form})

@login_required
def document_list(request):
    documents = Document.objects.all()
    # Log temporal para depuración
    logger.warning(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', None)}")
    if documents:
        logger.warning(f"Primer doc file.url: {getattr(documents[0].file, 'url', None)}")
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')

    if q:
        documents = documents.filter(
            models.Q(title__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(category__icontains=q) |
            models.Q(uploaded_at__icontains=q)
        )
    if category:
        documents = documents.filter(category=category)

    # Obtener las categorías del modelo
    category_choices = Document.CATEGORY_CHOICES

    return render(request, 'documents.html', {
        'documents': documents,
        'q': q,
        'selected_category': category,
        'category_choices': category_choices,
        'messages': messages.get_messages(request),
    })

@login_required
def edit_document(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento actualizado correctamente.')
            return redirect('documents:document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'documents/create.html', {'form': form, 'edit': True})

@login_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == 'POST':
        document.file.delete(save=False)  # Borra el archivo del storage
        document.delete()
        messages.success(request, 'Documento eliminado correctamente.')
        return redirect('documents:document_list')
    return render(request, 'documents/confirm_delete.html', {'document': document})

@login_required
def download_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    sas_url = document.sas_url
    if not sas_url:
        return render(request, 'documents/download_error.html', {'document': document, 'error': 'No se pudo generar la URL de descarga.'})
    try:
        azure_response = requests.get(sas_url, stream=True, timeout=10)
        if azure_response.status_code == 404:
            return render(request, 'documents/download_error.html', {'document': document, 'error': 'El archivo no existe en Azure Blob Storage.'})
        elif not azure_response.ok:
            return render(request, 'documents/download_error.html', {'document': document, 'error': f'Error al descargar el archivo: {azure_response.status_code}'})
        filename = document.file.name.split('/')[-1]
        response = HttpResponse(azure_response.raw, content_type=azure_response.headers.get('Content-Type', 'application/octet-stream'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        return render(request, 'documents/download_error.html', {'document': document, 'error': f'Error inesperado: {str(e)}'})
