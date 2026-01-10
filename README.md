# FuelCost Tracker

Веб-сервис для учета и анализа расходов на топливо автомобилистами. Позволяет отслеживать историю заправок, анализировать расход топлива и контролировать затраты.

**Ссылка на рабочий проект:** https://логин.pythonanywhere.com

## Возможности
- Учет заправок по каждому автомобилю
- Управление несколькими автомобилями
- Анализ расходов и статистика
- Автоматический расчет стоимости
- Адаптивный дизайн для мобильных устройств

## Технологии
* **Python 3.10**
* **Django 4.2**
* **Bootstrap 5** (интерфейс)
* **SQLite** (база данных)
* **Requests** (работа с API)

## Установка и запуск

### 1. Клонирование репозитория
\`\`\`bash
git clone https://github.com//fuelcost_tracker.git
cd fuelcost_tracker
\`\`\`

### 2. Создание виртуального окружения
\`\`\`bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
\`\`\`

### 3. Установка зависимостей
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Настройка базы данных
\`\`\`bash
python manage.py migrate
python manage.py createsuperuser
\`\`\`

### 5. Запуск сервера
\`\`\`bash
python manage.py runserver
\`\`\`

### 6. Открытие в браузере
Перейдите по адресу: http://127.0.0.1:8000/

## Структура проекта
\`\`\`
fuelcost_tracker/
├── tracker/          # Основное приложение
├── users/           # Приложение пользователей
├── templates/       # HTML шаблоны
├── manage.py        # Django CLI
└── requirements.txt # Зависимости
\`\`\`

## Скриншоты
(Скриншоты главной страницы, дашборда, статистики)

## Ссылка на рабочий проект
https://логин.pythonanywhere.com"