# -*- coding: utf-8 -*-
"""
Головний файл додатку
Ініціалізує Flask додаток та реєструє всі модулі
"""

# Імпорт основного класу Flask
from flask import Flask
# Імпорт конфігурації проекту
from Project.settings import Config
# Імпорт функції для завантаження змінних оточення
from Project.loadenv import load_environment

# Імпорт blueprints з різних модулів
from home.views import home_bp
from exoplanets.views import exoplanets_bp
from analytics.views import analytics_bp
from user.views import user_bp

# Імпорт модуля для роботи з файловою системою
import os

def create_app():
    """
    Фабрика для створення Flask додатку
    Ініціалізує та налаштовує додаток
    
    Повертає:
        Flask: Налаштований Flask додаток
    """
    # Завантажуємо змінні оточення з .env файлу
    load_environment()
    
    # Створюємо екземпляр Flask додатку
    app = Flask(__name__)
    # Завантажуємо конфігурацію з класу Config
    app.config.from_object(Config)
    
    # Реєструємо blueprints (модулі додатку)
    # Blueprint для головної сторінки
    app.register_blueprint(home_bp)
    # Blueprint для роботи з екзопланетами з префіксом /exoplanets
    app.register_blueprint(exoplanets_bp, url_prefix='/exoplanets')
    # Blueprint для аналітики з префіксом /analytics
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    # Blueprint для користувачів з префіксом /user
    app.register_blueprint(user_bp, url_prefix='/user')
    
    # Створюємо необхідні директорії якщо вони не існують
    # Директорія для збереження даних
    os.makedirs('data', exist_ok=True)
    # Директорія для зображень
    os.makedirs('static/images', exist_ok=True)
    # Директорія для кешу
    os.makedirs('cache', exist_ok=True)
    
    # Виводимо повідомлення про успішну ініціалізацію
    print("✓ Додаток успішно ініціалізовано")
    print(f"✓ Зареєстровано {len(app.blueprints)} модулів")
    
    # Повертаємо налаштований додаток
    return app

# Точка входу в програму
if __name__ == '__main__':
    # Створюємо додаток
    app = create_app()
    # Запускаємо сервер розробки
    # debug=True - режим відладки з автоперезавантаженням
    # host='0.0.0.0' - доступ з будь-якої IP адреси
    # port=9000 - порт на якому працює сервер
    app.run(debug=True, host='0.0.0.0', port=9000)
