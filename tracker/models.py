from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal

class Car(models.Model):
    FUEL_TYPES = [
        ('AI-92', 'АИ-92'),
        ('AI-95', 'АИ-95'),
        ('AI-98', 'АИ-98'),
        ('DIESEL', 'Дизель'),
        ('GAS', 'Газ'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    brand = models.CharField(max_length=50, verbose_name='Марка')
    model = models.CharField(max_length=50, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Год выпуска')
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPES, verbose_name='Тип топлива')
    engine_volume = models.FloatField(verbose_name='Объем двигателя (л)')
    average_consumption = models.FloatField(
        verbose_name='Средний расход (л/100км)',
        validators=[MinValueValidator(0.1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.brand} {self.model} ({self.year})'
    
    def get_total_fuel_cost(self):
        """Общая стоимость топлива для этой машины"""
        total = sum(refuel.total_cost for refuel in self.refuels.all())
        return total or 0
    
    def get_total_fuel_volume(self):
        """Общий объем заправленного топлива"""
        total = sum(refuel.volume for refuel in self.refuels.all())
        return total or 0

class Refuel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refuels')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='refuels')
    date = models.DateField(default=timezone.now, verbose_name='Дата заправки')
    odometer = models.IntegerField(verbose_name='Пробег (км)', validators=[MinValueValidator(0)])

    volume = models.DecimalField(verbose_name='Объем', max_digits=10, decimal_places=2)
    price_per_liter = models.DecimalField(verbose_name='Цена за литр', max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(verbose_name='Итоговая стоимость', max_digits=10, decimal_places=2, editable=False)

    full_tank = models.BooleanField(default=True, verbose_name='Полный бак')
    station_name = models.CharField(max_length=100, blank=True, verbose_name='Название АЗС')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_cost = self.volume * self.price_per_liter
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def save(self, *args, **kwargs):
        # Автоматический расчет общей стоимости
        self.total_cost = self.volume * self.price_per_liter
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Заправка {self.car} - {self.date}'
    
    def calculate_consumption(self):
        """Расчет расхода между заправками"""
        previous = Refuel.objects.filter(
            car=self.car,
            date__lt=self.date
        ).order_by('-date').first()
        
        if previous and previous.odometer < self.odometer and self.full_tank:
            distance = self.odometer - previous.odometer
            if distance > 0:
                consumption = (self.volume / distance) * 100
                return round(consumption, 2)
        return None

class FuelPrice(models.Model):
    """Модель для хранения цен на топливо из API"""
    fuel_type = models.CharField(max_length=10, choices=Car.FUEL_TYPES, verbose_name='Тип топлива')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Средняя цена (руб)')
    region = models.CharField(max_length=100, default='Москва', verbose_name='Регион')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    source = models.CharField(max_length=50, default='API', verbose_name='Источник')
    
    class Meta:
        ordering = ['fuel_type']
        unique_together = ['fuel_type', 'region']
    
    def __str__(self):
        return f'{self.get_fuel_type_display()} - {self.price} руб ({self.region})'