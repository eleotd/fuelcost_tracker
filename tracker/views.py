from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm

def home(request):
    return render(request, 'tracker/home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def car_list(request):
    return render(request, 'tracker/car_list.html')