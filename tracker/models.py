from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    FUEL_TYPES = [
        ('AI-92', 'АИ-92'),
        ('AI-95', 'АИ-95'),
        ('AI-98', 'АИ-98'),
        ('diesel', 'Дизель'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    engine_volume = models.FloatField()
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPES)
    
    def __str__(self):
        return f'{self.brand} {self.model}'

class Refueling(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    liters = models.FloatField()
    price_per_liter = models.DecimalField(max_digits=5, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField()
    full_tank = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f'Заправка {self.car} - {self.date}'

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name