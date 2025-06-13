# apps/directory/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Contact
from .forms import ContactForm
from django.db import models

def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contacto guardado correctamente.")
            return redirect('directory:list')
    else:
        form = ContactForm()
    return render(request, 'directory/create.html', {'form': form})


def contact_list(request):
    q = request.GET.get('q', '').strip()
    ministry = request.GET.get('ministry', '').strip()
    contacts = Contact.objects.all()
    if q:
        contacts = contacts.filter(
            models.Q(name__icontains=q) |
            models.Q(role__icontains=q) |
            models.Q(ministry__icontains=q) |
            models.Q(contact__icontains=q)
        )
    if ministry:
        contacts = contacts.filter(ministry__icontains=ministry)
    ministries = Contact.objects.values_list('ministry', flat=True).distinct()
    return render(request, 'directory/directory.html', {
        'contacts': contacts,
        'q': q,
        'ministries': ministries,
        'selected_ministry': ministry,
    })


def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contacto actualizado correctamente.")
            return redirect('directory:list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'directory/edit.html', {'form': form, 'contact': contact})


def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "Contacto eliminado correctamente.")
        return redirect('directory:list')
    return render(request, 'directory/delete.html', {'contact': contact})
