from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Avg, Count, Min, Max
from django.contrib.humanize.templatetags.humanize import intcomma
import requests
from datetime import datetime, timedelta
from .models import Car, Refuel, FuelPrice
from .forms import CarForm, RefuelForm
from .api_client import get_fuel_prices_from_api, update_fuel_prices_in_db  # Импорт API клиента

def home(request):
    """Главная страница"""
    context = {
        'title': 'Главная'
    }
    return render(request, 'tracker/home.html', context)

@login_required
def dashboard(request):
    """Панель управления"""
    user_cars = Car.objects.filter(user=request.user)
    recent_refuels = Refuel.objects.filter(user=request.user).order_by('-date')[:5]

    total_spent = Refuel.objects.filter(user=request.user).aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    total_volume = Refuel.objects.filter(user=request.user).aggregate(Sum('volume'))['volume__sum'] or 0
    avg_price = Refuel.objects.filter(user=request.user).aggregate(Avg('price_per_liter'))['price_per_liter__avg'] or 0
    
    context = {
        'title': 'Панель управления',
        'cars': user_cars,
        'recent_refuels': recent_refuels,
        'total_spent': total_spent,
        'total_volume': total_volume,
        'avg_price': round(avg_price, 2),
        'car_count': user_cars.count(),
        'refuel_count': Refuel.objects.filter(user=request.user).count(),
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def car_list(request):
    """Список автомобилей"""
    cars = Car.objects.filter(user=request.user)
    
    total_spent = 0
    total_refuels = 0
    total_volume = 0
    
    for car in cars:
        total_spent += car.get_total_fuel_cost() or 0
        total_volume += car.get_total_fuel_volume() or 0
        total_refuels += car.refuels.count()
    
    avg_per_car = total_spent / cars.count() if cars.count() > 0 else 0
    avg_refuels_per_car = total_refuels / cars.count() if cars.count() > 0 else 0
    
    context = {
        'title': 'Мои автомобили',
        'cars': cars,
        'total_spent': total_spent,
        'total_refuels': total_refuels,
        'avg_per_car': avg_per_car,
        'avg_refuels_per_car': avg_refuels_per_car,
    }
    return render(request, 'tracker/car_list.html', context)

@login_required
def car_add(request):
    """Добавление автомобиля"""
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()
            messages.success(request, 'Автомобиль успешно добавлен!')
            return redirect('car-list')
    else:
        form = CarForm()
    
    context = {
        'title': 'Добавить автомобиль',
        'form': form,
    }
    return render(request, 'tracker/car_form.html', context)

@login_required
def refuel_list(request):
    """Список заправок"""
    refuels = Refuel.objects.filter(user=request.user).select_related('car')

    car_id = request.GET.get('car')
    if car_id:
        refuels = refuels.filter(car_id=car_id)

    total_cost = refuels.aggregate(total=Sum('total_cost'))['total'] or 0
    total_volume = refuels.aggregate(total=Sum('volume'))['total'] or 0
    avg_price = refuels.aggregate(avg=Avg('price_per_liter'))['avg'] or 0
    avg_volume = refuels.aggregate(avg=Avg('volume'))['avg'] or 0
    
    context = {
        'title': 'История заправок',
        'refuels': refuels,
        'cars': Car.objects.filter(user=request.user),
        'selected_car': car_id,
        'total_cost': total_cost,
        'total_volume': total_volume,
        'avg_price': avg_price,
        'avg_volume': avg_volume,
    }
    return render(request, 'tracker/refuel_list.html', context)

@login_required
def refuel_add(request):
    """Добавление заправки"""
    if request.method == 'POST':
        form = RefuelForm(request.user, request.POST)
        if form.is_valid():
            refuel = form.save(commit=False)
            refuel.user = request.user
            refuel.save()
            messages.success(request, 'Заправка успешно добавлена!')
            return redirect('refuel-list')
    else:
        form = RefuelForm(user=request.user)
    
    context = {
        'title': 'Добавить заправку',
        'form': form,
    }
    return render(request, 'tracker/refuel_form.html', context)

@login_required
def refuel_edit(request, pk):
    """Редактирование заправки"""
    refuel = get_object_or_404(Refuel, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = RefuelForm(request.user, request.POST, instance=refuel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заправка успешно обновлена!')
            return redirect('refuel-list')
    else:
        form = RefuelForm(user=request.user, instance=refuel)
    
    context = {
        'title': 'Редактировать заправку',
        'form': form,
        'refuel': refuel,
    }
    return render(request, 'tracker/refuel_form.html', context)

@login_required
def refuel_delete(request, pk):
    """Удаление заправки"""
    refuel = get_object_or_404(Refuel, pk=pk, user=request.user)
    
    if request.method == 'POST':
        refuel.delete()
        messages.success(request, 'Заправка удалена!')
        return redirect('refuel-list')
    
    context = {
        'title': 'Удалить заправку',
        'refuel': refuel,
    }
    return render(request, 'tracker/refuel_confirm_delete.html', context)

@login_required
def statistics(request):
    """Страница статистики с графиками"""
    refuels = Refuel.objects.filter(user=request.user).select_related('car')
    cars = Car.objects.filter(user=request.user)
    
    total_stats = {
        'spent': refuels.aggregate(Sum('total_cost'))['total_cost__sum'] or 0,
        'volume': refuels.aggregate(Sum('volume'))['volume__sum'] or 0,
        'count': refuels.count(),
        'avg_price': refuels.aggregate(Avg('price_per_liter'))['price_per_liter__avg'] or 0,
    }
    
    monthly_data = []
    for i in range(5, -1, -1):
        month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        
        month_refuels = refuels.filter(date__range=[month_start, month_end])
        monthly_spent = month_refuels.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        
        monthly_data.append({
            'month': month_start.strftime('%b %Y'),
            'spent': float(monthly_spent),
            'count': month_refuels.count(),
        })

    MONTHLY_BUDGET = 5000
    
    for item in monthly_data:
        if MONTHLY_BUDGET > 0:
            percent = min(100, int((item['spent'] / MONTHLY_BUDGET) * 100))
        else:
            percent = 0
        item['percent'] = percent
        
        item['is_complete'] = percent >= 100  
    
    car_stats = []
    for car in cars:
        car_refuels = refuels.filter(car=car)
        car_total = car_refuels.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        car_volume = car_refuels.aggregate(Sum('volume'))['volume__sum'] or 0
        
        if car_refuels.count() > 1:
            first_refuel = car_refuels.order_by('date').first()
            last_refuel = car_refuels.order_by('date').last()
            
            if first_refuel and last_refuel and last_refuel.odometer > first_refuel.odometer:
                total_distance = last_refuel.odometer - first_refuel.odometer
                total_fuel = sum(r.volume for r in car_refuels if r != last_refuel)
                
                if total_distance > 0 and total_fuel > 0:
                    avg_consumption = (total_fuel / total_distance) * 100
                else:
                    avg_consumption = car.average_consumption
            else:
                avg_consumption = car.average_consumption
        else:
            avg_consumption = car.average_consumption
        
        car_stats.append({
            'car': car,
            'total_spent': car_total,
            'total_volume': car_volume,
            'refuel_count': car_refuels.count(),
            'avg_consumption': round(avg_consumption, 2),
        })
    
    fuel_prices = [
        {'type': 'AI-92', 'price': 48.50},
        {'type': 'AI-95', 'price': 52.30},
        {'type': 'AI-98', 'price': 58.90},
        {'type': 'DIESEL', 'price': 55.40},
    ]
    
    context = {
        'title': 'Статистика',
        'total_stats': total_stats,
        'monthly_data': monthly_data,
        'car_stats': car_stats,
        'fuel_prices': fuel_prices,
        'cars': cars,
        'monthly_budget': MONTHLY_BUDGET,
    }
    return render(request, 'tracker/statistics.html', context)