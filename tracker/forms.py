from django import forms
from django.contrib.auth.models import User
from .models import Car, Refuel

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'fuel_type', 'engine_volume', 'average_consumption']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Toyota'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Camry'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1990, 'max': 2024}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'engine_volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0.5'}),
            'average_consumption': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '3'}),
        }
        labels = {
            'engine_volume': 'Объем двигателя (литры)',
            'average_consumption': 'Средний расход (литров на 100 км)',
        }

class RefuelForm(forms.ModelForm):
    class Meta:
        model = Refuel
        fields = ['car', 'date', 'odometer', 'volume', 'price_per_liter', 'full_tank', 'station_name', 'notes']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'odometer': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0.1'}),
            'price_per_liter': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'full_tank': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'station_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название АЗС'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарии...'}),
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['car'].queryset = Car.objects.filter(user=user)