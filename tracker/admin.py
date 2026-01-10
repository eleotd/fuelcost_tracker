from django.contrib import admin
from .models import Car, Refueling, ExpenseCategory

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'fuel_type', 'user')
    list_filter = ('fuel_type', 'year')

@admin.register(Refueling)
class RefuelingAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'liters', 'price_per_liter', 'total_cost')
    list_filter = ('date', 'car')

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')