from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Car, Refueling

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'engine_volume', 'fuel_type']
        widgets = {
            'year': forms.NumberInput(attrs={'min': 1990, 'max': 2024}),
        }

class RefuelingForm(forms.ModelForm):
    class Meta:
        model = Refueling
        fields = ['car', 'date', 'liters', 'price_per_liter', 'mileage', 'full_tank']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }