from flask import Blueprint, jsonify, request
from services.exoplanet_service import ExoplanetService
from services.habitability_calculator import HabitabilityCalculator
import time

api_bp = Blueprint('api', __name__)
exoplanet_service = ExoplanetService()
calculator = HabitabilityCalculator()

@api_bp.route('/planets', methods=['GET'])
def get_planets():
    """API endpoint для отримання списку планет"""
    try:
        limit = request.args.get('limit', 100, type=int)
        min_habitability = request.args.get('min_habitability', 0, type=float)
        
        start_time = time.time()
        
        planets_df = exoplanet_service.get_planets_data()
        
        if planets_df is None:
            return jsonify({'error': 'Не вдалося завантажити дані'}), 500
        
        planets_df = calculator.calculate_batch(planets_df)
        
        if min_habitability > 0:
            planets_df = planets_df[planets_df['habitability_index'] >= min_habitability]
        
        planets_df = planets_df.sort_values('habitability_index', ascending=False)
        planets = planets_df.head(limit).to_dict('records')
        
        processing_time = time.time() - start_time
        
        return jsonify({
            'count': len(planets),
            'planets': planets,
            'processing_time': f'{processing_time:.3f}s'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/planet/<planet_name>', methods=['GET'])
def get_planet_detail(planet_name):
    """API endpoint для детальної інформації про планету"""
    try:
        planets_df = exoplanet_service.get_planets_data()
        planets_df = calculator.calculate_batch(planets_df)
        
        planet_data = planets_df[planets_df['pl_name'] == planet_name]
        
        if planet_data.empty:
            return jsonify({'error': 'Планету не знайдено'}), 404
        
        planet = planet_data.iloc[0].to_dict()
        components = calculator.get_components(planet)
        
        return jsonify({
            'planet': planet,
            'habitability_components': components
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stats', methods=['GET'])
def get_statistics():
    """API endpoint для статистики"""
    try:
        start_time = time.time()
        
        planets_df = exoplanet_service.get_planets_data()
        planets_df = calculator.calculate_batch(planets_df)
        
        stats = {
            'total_planets': len(planets_df),
            'avg_habitability': float(planets_df['habitability_index'].mean()),
            'max_habitability': float(planets_df['habitability_index'].max()),
            'min_habitability': float(planets_df['habitability_index'].min()),
            'top_10_planets': planets_df.nlargest(10, 'habitability_index')['pl_name'].tolist(),
            'discovery_methods': planets_df['discoverymethod'].value_counts().to_dict(),
            'processing_time': f'{time.time() - start_time:.3f}s'
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/compare', methods=['POST'])
def compare_planets():
    """API для порівняння планет"""
    try:
        data = request.get_json()
        planet_names = data.get('planets', [])
        
        if not planet_names:
            return jsonify({'error': 'Не вказано планети для порівняння'}), 400
        
        planets_df = exoplanet_service.get_planets_data()
        planets_df = calculator.calculate_batch(planets_df)
        
        compared = planets_df[planets_df['pl_name'].isin(planet_names)]
        
        if compared.empty:
            return jsonify({'error': 'Планети не знайдено'}), 404
        
        comparison = {
            'planets': compared.to_dict('records'),
            'summary': {
                'avg_habitability': float(compared['habitability_index'].mean()),
                'best_planet': compared.nlargest(1, 'habitability_index')['pl_name'].iloc[0]
            }
        }
        
        return jsonify(comparison)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
