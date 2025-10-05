from flask import Blueprint, render_template, jsonify
from services.exoplanet_service import ExoplanetService
from services.habitability_calculator import HabitabilityCalculator
from services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__)
exoplanet_service = ExoplanetService()
calculator = HabitabilityCalculator()
analytics_service = AnalyticsService()

@analytics_bp.route('/')
def analytics_dashboard():
    """Дашборд аналітики"""
    return render_template('analytics/dashboard.html')

@analytics_bp.route('/data/distribution')
def habitability_distribution():
    """Розподіл індексу придатності"""
    try:
        planets_df = exoplanet_service.get_planets_data()
        planets_df = calculator.calculate_batch(planets_df)
        
        distribution = analytics_service.get_habitability_distribution(planets_df)
        
        return jsonify(distribution)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/data/parameters-correlation')
def parameters_correlation():
    """Кореляція параметрів"""
    try:
        planets_df = exoplanet_service.get_planets_data()
        planets_df = calculator.calculate_batch(planets_df)
        
        correlation = analytics_service.get_parameters_correlation(planets_df)
        
        return jsonify(correlation)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/data/discovery-timeline')
def discovery_timeline():
    """Часова шкала відкриттів"""
    try:
        planets_df = exoplanet_service.get_planets_data()
        planets_df = calculator.calculate_batch(planets_df)
        
        timeline = analytics_service.get_discovery_timeline(planets_df)
        
        return jsonify(timeline)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/data/top-habitable')
def top_habitable_planets():
    """Топ найпридатніших планет"""
    try:
        planets_df = exoplanet_service.get_planets_data()
        planets_df = calculator.calculate_batch(planets_df)
        
        top_planets = analytics_service.get_top_habitable_planets(planets_df, top_n=20)
        
        return jsonify(top_planets)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/data/method-comparison')
def method_comparison():
    """Порівняння методів відкриття"""
    try:
        planets_df = exoplanet_service.get_planets_data()
        planets_df = calculator.calculate_batch(planets_df)
        
        comparison = analytics_service.get_discovery_method_comparison(planets_df)
        
        return jsonify(comparison)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
