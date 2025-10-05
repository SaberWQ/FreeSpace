# -*- coding: utf-8 -*-
"""
Views (представлення) для модуля home
Обробляє запити до головної сторінки
"""

# Імпорт необхідних компонентів Flask
from flask import Blueprint, render_template, request, jsonify

# Створюємо Blueprint для модуля home
# Blueprint - це спосіб організації маршрутів у Flask
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    """
    Головна сторінка додатку
    
    Маршрут: /
    Метод: GET
    
    Повертає:
        HTML: Відрендерений шаблон головної сторінки
    """
    # Рендеримо та повертаємо головний шаблон
    return render_template('index.html')

@home_bp.route('/about')
def about():
    """
    Сторінка "Про проект"
    
    Маршрут: /about
    Метод: GET
    
    Повертає:
        HTML: Інформація про проект
    """
    # Дані про проект
    project_info = {
        'name': 'Exoplanet Habitability Analytics',
        'version': '1.0.0',
        'description': 'Аналіз придатності екзопланет для життя',
        'author': 'Exoplanet Research Team'
    }
    
    # Рендеримо шаблон з інформацією про проект
    return render_template('about.html', info=project_info)
