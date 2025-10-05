# -*- coding: utf-8 -*-
"""
Views (представлення) для модуля analytics
Обробляє запити для аналітики та візуалізації
"""

# Імпорт необхідних компонентів Flask
from flask import Blueprint, render_template, jsonify
# Імпорт сервісу для роботи з екзопланетами
from exoplanets.services import ExoplanetService
# Імпорт калькулятора придатності
from exoplanets.habitability import HabitabilityCalculator
# Імпорт сервісу аналітики
from analytics.services import AnalyticsService

from concurrent.futures import ThreadPoolExecutor
import asyncio

# Створюємо Blueprint для модуля analytics
analytics_bp = Blueprint('analytics', __name__)

# Ініціалізуємо необхідні сервіси
exoplanet_service = ExoplanetService()
calculator = HabitabilityCalculator()
analytics_service = AnalyticsService()

executor = ThreadPoolExecutor(max_workers=4)

def load_and_calculate_data():
    """Helper function to load and calculate data in thread pool"""
    planets_df = exoplanet_service.get_planets_data()
    if planets_df is None or planets_df.empty:
        return None
    return calculator.calculate_batch(planets_df)

@analytics_bp.route('/dashboard')
def dashboard():
    """
    Головна сторінка аналітики з дашбордом
    
    Маршрут: /analytics/dashboard
    Метод: GET
    
    Повертає:
        HTML: Сторінка з дашбордом та графіками
    """
    try:
        # Завантажуємо дані про планети
        planets_df = exoplanet_service.get_planets_data()
        
        # Перевіряємо чи дані завантажились
        if planets_df is None or planets_df.empty:
            return render_template('analytics/dashboard.html', 
                                 error="Не вдалося завантажити дані")
        
        # Розраховуємо індекс придатності для всіх планет
        planets_df = calculator.calculate_batch(planets_df)
        
        # Отримуємо базову статистику
        stats = {
            'total_planets': len(planets_df),  # Загальна кількість планет
            'avg_habitability': round(planets_df['habitability_index'].mean(), 2),  # Середній індекс
            'max_habitability': round(planets_df['habitability_index'].max(), 2),  # Максимальний індекс
            'habitable_count': len(planets_df[planets_df['habitability_index'] >= 50])  # Кількість придатних
        }
        
        # Рендеримо шаблон дашборду зі статистикою
        return render_template('analytics/dashboard.html', 
                             stats=stats, 
                             error=None)
    
    except Exception as e:
        # У разі помилки повертаємо сторінку з повідомленням
        return render_template('analytics/dashboard.html', 
                             error=str(e))

@analytics_bp.route('/api/habitability-distribution')
def habitability_distribution():
    """
    API для отримання розподілу індексу придатності
    
    Маршрут: /analytics/api/habitability-distribution
    Метод: GET
    
    Повертає:
        JSON: Дані для побудови графіка розподілу
    """
    try:
        planets_df = load_and_calculate_data()
        
        if planets_df is None:
            return jsonify({'error': 'Не вдалося завантажити дані'}), 500
        
        # Отримуємо дані розподілу
        distribution = analytics_service.get_habitability_distribution(planets_df)
        
        # Повертаємо дані у форматі JSON
        return jsonify(distribution)
    
    except Exception as e:
        # У разі помилки повертаємо JSON з помилкою
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/parameters-correlation')
def parameters_correlation():
    """
    API для отримання кореляції параметрів
    
    Маршрут: /analytics/api/parameters-correlation
    Метод: GET
    
    Повертає:
        JSON: Дані про кореляцію параметрів з індексом придатності
    """
    try:
        planets_df = load_and_calculate_data()
        
        if planets_df is None:
            return jsonify({'error': 'Не вдалося завантажити дані'}), 500
        
        # Отримуємо дані кореляції
        correlation = analytics_service.get_parameters_correlation(planets_df)
        
        # Повертаємо дані у форматі JSON
        return jsonify(correlation)
    
    except Exception as e:
        # У разі помилки повертаємо JSON з помилкою
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/discovery-timeline')
def discovery_timeline():
    """
    API для отримання часової шкали відкриттів
    
    Маршрут: /analytics/api/discovery-timeline
    Метод: GET
    
    Повертає:
        JSON: Дані про відкриття планет по роках
    """
    try:
        planets_df = load_and_calculate_data()
        
        if planets_df is None:
            return jsonify({'error': 'Не вдалося завантажити дані'}), 500
        
        # Отримуємо дані часової шкали
        timeline = analytics_service.get_discovery_timeline(planets_df)
        
        # Повертаємо дані у форматі JSON
        return jsonify(timeline)
    
    except Exception as e:
        # У разі помилки повертаємо JSON з помилкою
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/top-habitable')
def top_habitable():
    """
    API для отримання топ найпридатніших планет
    
    Маршрут: /analytics/api/top-habitable
    Метод: GET
    
    Повертає:
        JSON: Список топ-20 найпридатніших планет
    """
    try:
        planets_df = load_and_calculate_data()
        
        if planets_df is None:
            return jsonify({'error': 'Не вдалося завантажити дані'}), 500
        
        # Отримуємо топ планет
        top_planets = analytics_service.get_top_habitable_planets(planets_df, top_n=20)
        
        # Повертаємо дані у форматі JSON
        return jsonify(top_planets)
    
    except Exception as e:
        # У разі помилки повертаємо JSON з помилкою
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/discovery-methods')
def discovery_methods():
    """
    API для порівняння методів відкриття
    
    Маршрут: /analytics/api/discovery-methods
    Метод: GET
    
    Повертає:
        JSON: Статистика по методах відкриття планет
    """
    try:
        planets_df = load_and_calculate_data()
        
        if planets_df is None:
            return jsonify({'error': 'Не вдалося завантажити дані'}), 500
        
        # Отримуємо порівняння методів
        methods = analytics_service.get_discovery_method_comparison(planets_df)
        
        # Повертаємо дані у форматі JSON
        return jsonify(methods)
    
    except Exception as e:
        # У разі помилки повертаємо JSON з помилкою
        return jsonify({'error': str(e)}), 500
