"""
Модуль для работы с внешними API цен на топливо
В демо-версии использует фиктивные данные
"""

def get_fuel_prices_from_api():
    """
    Получение цен на топливо из внешнего источника
    В реальной версии здесь будет интеграция с настоящим API
    """
    # Фиктивные данные для демонстрации
    fuel_prices = [
        {'type': 'AI-92', 'price': 48.50, 'region': 'Москва', 'source': 'Демо'},
        {'type': 'AI-95', 'price': 52.30, 'region': 'Москва', 'source': 'Демо'},
        {'type': 'AI-98', 'price': 58.90, 'region': 'Москва', 'source': 'Демо'},
        {'type': 'DIESEL', 'price': 55.40, 'region': 'Москва', 'source': 'Демо'},
        {'type': 'GAS', 'price': 32.10, 'region': 'Москва', 'source': 'Демо'},
    ]
    
    return fuel_prices


def update_fuel_prices_in_db():
    """
    Обновление цен в базе данных из внешнего источника
    """
    from .models import FuelPrice
    
    try:
        prices = get_fuel_prices_from_api()
        
        for price_data in prices:
            fuel_price, created = FuelPrice.objects.update_or_create(
                fuel_type=price_data['type'],
                region=price_data['region'],
                defaults={
                    'price': price_data['price'],
                    'source': price_data['source']
                }
            )
        
        return True, f"Обновлено {len(prices)} записей"
    except Exception as e:
        return False, f"Ошибка обновления: {str(e)}"