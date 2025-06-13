from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import Donation
from .forms import DonationForm

@login_required
def donation_list(request):
    """
    Vista principal que muestra las donaciones activas, ordenadas por fecha de creación.
    Incluye búsqueda por título, tipo y entidad.
    """
    query = request.GET.get('q', '').strip()
    donation_type = request.GET.get('type', '').strip()
    
    donations = Donation.objects.all()
    
    if query:
        donations = donations.filter(
            Q(title__icontains=query) |
            Q(type__icontains=query) |
            Q(entity__icontains=query) |
            Q(description__icontains=query)
        )
    
    if donation_type:
        donations = donations.filter(type=donation_type)
    
    context = {
        'donations': donations,
        'query': query,
        'selected_type': donation_type,
        'donation_types': Donation.TYPE_CHOICES,
    }
    
    return render(request, 'donations/donations.html', context)

@login_required
def donation_create(request):
    """
    Vista que permite crear una nueva donación.
    Asigna automáticamente el usuario actual como creador.
    """
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.created_by = request.user
            donation.save()
            messages.success(request, 'Donación creada exitosamente.')
            return redirect('donations:list')
    else:
        form = DonationForm()
    
    return render(request, 'donations/donation_form.html', {
        'form': form,
        'action': 'Crear'
    })

@login_required
def donation_edit(request, pk):
    """
    Vista que permite editar una donación existente.
    Solo permite editar al creador o superusuarios.
    """
    donation = get_object_or_404(Donation, pk=pk)
    
    if not request.user.is_superuser and donation.created_by != request.user:
        messages.error(request, 'No tienes permiso para editar esta donación.')
        return redirect('donations:list')

    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donación actualizada exitosamente.')
            return redirect('donations:list')
    else:
        form = DonationForm(instance=donation)
    
    return render(request, 'donations/donation_form.html', {
        'form': form,
        'donation': donation,
        'action': 'Editar'
    })

@login_required
def donation_delete(request, pk):
    """
    Vista que permite eliminar una donación.
    Solo permite eliminar al creador o superusuarios.
    """
    donation = get_object_or_404(Donation, pk=pk)
    
    if not request.user.is_superuser and donation.created_by != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta donación.')
        return redirect('donations:list')

    if request.method == 'POST':
        donation.delete()
        messages.success(request, 'Donación eliminada exitosamente.')
        return redirect('donations:list')
    
    return render(request, 'donations/donation_confirm_delete.html', {
        'donation': donation
    })
