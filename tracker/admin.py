from django.contrib import admin
from .models import Car, Refuel, FuelPrice

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'fuel_type', 'user', 'created_at')
    list_filter = ('fuel_type', 'year', 'created_at')
    search_fields = ('brand', 'model', 'user__username')
    readonly_fields = ('created_at',)

@admin.register(Refuel)
class RefuelAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'odometer', 'volume', 'price_per_liter', 'total_cost', 'user')
    list_filter = ('date', 'car', 'full_tank')
    search_fields = ('car__brand', 'car__model', 'station_name', 'notes')
    readonly_fields = ('total_cost', 'created_at')
    date_hierarchy = 'date'

@admin.register(FuelPrice)
class FuelPriceAdmin(admin.ModelAdmin):
    list_display = ('fuel_type', 'price', 'region', 'date_updated', 'source')
    list_filter = ('fuel_type', 'region')
    readonly_fields = ('date_updated',)