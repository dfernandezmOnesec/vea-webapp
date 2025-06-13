from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render

def index_view(request):
    return render(request, 'core/index.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente tras registrar
            return redirect('dashboard:home')  # Redirige al dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
