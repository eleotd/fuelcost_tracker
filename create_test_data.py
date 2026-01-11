"""
Скрипт для создания тестовых данных в базе данных
Запуск: python create_test_data.py
"""

import os
import django
import random
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuelcost_project.settings')
django.setup()

from django.contrib.auth.models import User
from tracker.models import Car, Refuel, FuelPrice

def create_test_data():
    """Создание тестовых данных"""
    
    print("=" * 50)
    print("Создание тестовых данных для FuelCost Tracker")
    print("=" * 50)
    
    # 1. Создаем тестового пользователя
    user, created = User.objects.get_or_create(
        username='demo_user',
        defaults={
            'email': 'demo@example.com',
            'first_name': 'Демо',
            'last_name': 'Пользователь'
        }
    )
    
    if created:
        user.set_password('demo123')
        user.save()
        print(f"✅ Создан пользователь: {user.username} (пароль: demo123)")
    else:
        print(f"⚠️  Пользователь {user.username} уже существует")
    
    # 2. Создаем автомобили
    cars_data = [
        {
            'brand': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'fuel_type': 'AI-95',
            'engine_volume': 2.5,
            'average_consumption': 8.5
        },
        {
            'brand': 'Hyundai',
            'model': 'Solaris',
            'year': 2019,
            'fuel_type': 'AI-92',
            'engine_volume': 1.6,
            'average_consumption': 7.2
        },
        {
            'brand': 'Skoda',
            'model': 'Octavia',
            'year': 2021,
            'fuel_type': 'AI-95',
            'engine_volume': 1.8,
            'average_consumption': 7.8
        },
        {
            'brand': 'Lada',
            'model': 'Vesta',
            'year': 2022,
            'fuel_type': 'AI-92',
            'engine_volume': 1.6,
            'average_consumption': 8.2
        },
        {
            'brand': 'KIA',
            'model': 'Rio',
            'year': 2020,
            'fuel_type': 'AI-95',
            'engine_volume': 1.6,
            'average_consumption': 7.5
        }
    ]
    
    cars = []
    for i, car_data in enumerate(cars_data):
        car, created = Car.objects.get_or_create(
            user=user,
            **car_data
        )
        cars.append(car)
        if created:
            print(f"✅ Создан автомобиль: {car.brand} {car.model}")
        else:
            print(f"⚠️  Автомобиль {car.brand} {car.model} уже существует")
    
    # 3. Создаем цены на топливо
    fuel_prices_data = [
        {'fuel_type': 'AI-92', 'price': 48.50, 'region': 'Москва', 'source': 'API'},
        {'fuel_type': 'AI-95', 'price': 52.30, 'region': 'Москва', 'source': 'API'},
        {'fuel_type': 'AI-98', 'price': 58.90, 'region': 'Москва', 'source': 'API'},
        {'fuel_type': 'DIESEL', 'price': 55.40, 'region': 'Москва', 'source': 'API'},
        {'fuel_type': 'GAS', 'price': 32.10, 'region': 'Москва', 'source': 'API'},
    ]
    
    for price_data in fuel_prices_data:
        fuel_price, created = FuelPrice.objects.update_or_create(
            fuel_type=price_data['fuel_type'],
            region=price_data['region'],
            defaults=price_data
        )
        if created:
            print(f"✅ Добавлена цена на {fuel_price.get_fuel_type_display()}: {fuel_price.price} руб")
    
    # 4. Создаем заправки для каждого автомобиля
    stations = ['Лукойл', 'Газпромнефть', 'Роснефть', 'Татнефть', 'Shell', 'BP', 'Газпром']
    
    # Цены по типам топлива для реалистичности
    fuel_price_map = {
        'AI-92': [46.50, 47.00, 47.50, 48.00, 48.50],
        'AI-95': [50.30, 50.80, 51.30, 51.80, 52.30],
        'AI-98': [56.90, 57.40, 57.90, 58.40, 58.90],
        'DIESEL': [53.40, 53.90, 54.40, 54.90, 55.40],
        'GAS': [30.10, 30.60, 31.10, 31.60, 32.10]
    }
    
    total_refuels = 0
    
    for car in cars:
        print(f"\n📝 Создаю заправки для {car.brand} {car.model}:")
        
        # Начальные значения
        odometer = random.randint(10000, 50000)
        start_date = datetime.now() - timedelta(days=180)  # 6 месяцев назад
        
        # Создаем 6-8 заправок для каждого авто
        num_refuels = random.randint(6, 8)
        
        for i in range(num_refuels):
            # Случайные параметры
            volume = round(random.uniform(30.0, 60.0), 1)
            price = random.choice(fuel_price_map[car.fuel_type])
            total_cost = round(volume * price, 2)
            
            # Создаем заправку
            refuel = Refuel.objects.create(
                user=user,
                car=car,
                date=start_date.date(),
                odometer=odometer,
                volume=volume,
                price_per_liter=price,
                total_cost=total_cost,
                full_tank=random.choice([True, False]),
                station_name=random.choice(stations),
                notes=random.choice([
                    f"Обычная заправка",
                    f"Заправка по пути на работу",
                    f"Заправка перед поездкой",
                    f"Акция на АЗС",
                    f"Ночная заправка",
                    ""
                ])
            )
            
            # Обновляем значения для следующей заправки
            odometer += random.randint(400, 800)
            start_date += timedelta(days=random.randint(7, 14))
            total_refuels += 1
            
            print(f"  ✅ Заправка {i+1}: {volume}л по {price}руб = {total_cost}руб")
    
    # 5. Статистика
    print("\n" + "=" * 50)
    print("📊 СТАТИСТИКА СОЗДАННЫХ ДАННЫХ:")
    print("=" * 50)
    print(f"👤 Пользователей: {User.objects.count()}")
    print(f"🚗 Автомобилей: {Car.objects.count()}")
    print(f"⛽ Заправок: {Refuel.objects.count()}")
    print(f"💰 Цен на топливо: {FuelPrice.objects.count()}")
    
    # Статистика по пользователю
    user_refuels = Refuel.objects.filter(user=user)
    total_spent = sum(refuel.total_cost for refuel in user_refuels)
    total_volume = sum(refuel.volume for refuel in user_refuels)
    
    print(f"\n📈 Для пользователя {user.username}:")
    print(f"   Всего потрачено: {total_spent:.2f} руб")
    print(f"   Всего топлива: {total_volume:.1f} л")
    print(f"   Средняя цена: {total_spent/total_volume:.2f} руб/л" if total_volume > 0 else "   Средняя цена: 0 руб/л")
    
    print("\n" + "=" * 50)
    print("🎉 ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО СОЗДАНЫ!")
    print("=" * 50)
    
    # Данные для входа
    print("\n🔐 ДАННЫЕ ДЛЯ ВХОДА:")
    print(f"   Логин: demo_user")
    print(f"   Пароль: demo123")
    print(f"   Или используйте созданного суперпользователя")
    
    print("\n🌐 Запустите сервер и откройте:")
    print("   http://127.0.0.1:8000/")

if __name__ == "__main__":
    create_test_data()