# apps/documents/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from .models import Document
import mimetypes
import datetime
from django.http import HttpResponseRedirect
from django.db import models

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()
            messages.success(request, f"El documento '{document.title}' se subió correctamente.")
            return redirect('documents:document_list')
    else:
        form = DocumentForm()
    return render(request, 'documents/create.html', {'form': form})

@login_required
def document_list(request):
    documents = Document.objects.all()
    q = request.GET.get('q', '').strip()
    categories = request.GET.getlist('category')

    if q:
        documents = documents.filter(
            models.Q(title__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(category__icontains=q) |
            models.Q(uploaded_at__icontains=q)
        )
    if categories:
        documents = documents.filter(category__in=categories)

    return render(request, 'documents.html', {
        'documents': documents,
        'q': q,
        'selected_categories': categories,
        'messages': messages.get_messages(request),
    })

@login_required
def edit_document(request, pk):
    document = get_object_or_404(Document, pk=pk, owner=request.user)
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
    document = get_object_or_404(Document, pk=pk, owner=request.user)
    if request.method == 'POST':
        document.file.delete(save=False)  # Borra el archivo del storage
        document.delete()
        messages.success(request, 'Documento eliminado correctamente.')
        return redirect('documents:document_list')
    return render(request, 'documents/confirm_delete.html', {'document': document})
