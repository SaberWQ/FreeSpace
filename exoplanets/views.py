# -*- coding: utf-8 -*-
"""
Views (представлення) для модуля exoplanets
Обробляє запити для роботи з екзопланетами з підтримкою async
"""

from flask import Blueprint, render_template, request, jsonify
from exoplanets.services import ExoplanetService
from exoplanets.habitability import HabitabilityCalculator
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

exoplanets_bp = Blueprint('exoplanets', __name__)

exoplanet_service = ExoplanetService()
calculator = HabitabilityCalculator()

executor = ThreadPoolExecutor(max_workers=4)

def async_route(f):
    """Декоратор для асинхронних маршрутів"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.close()
    return wrapper

async def load_planets_async():
    """Асинхронне завантаження даних про планети"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, exoplanet_service.get_planets_data)

async def calculate_habitability_async(planets_df):
    """Асинхронний розрахунок індексу придатності"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, calculator.calculate_batch, planets_df)

@exoplanets_bp.route('/planets')
@async_route
async def planets_list():
    """
    Список всіх екзопланет з фільтрацією (async версія)
    """
    try:
        min_habitability = request.args.get('min_habitability', 0, type=float)
        max_radius = request.args.get('max_radius', 10, type=float)
        discovery_method = request.args.get('discovery_method', '')
        page = request.args.get('page', 1, type=int)
        per_page = 50
        
        current_filters = {
            'min_habitability': min_habitability,
            'max_radius': max_radius,
            'discovery_method': discovery_method
        }
        
        planets_df = await load_planets_async()
        
        if planets_df is None or planets_df.empty:
            return render_template('planets.html', 
                                 planets=[], 
                                 error="Не вдалося завантажити дані", 
                                 pagination=None,
                                 discovery_methods=[],
                                 current_filters=current_filters)
        
        planets_df = await calculate_habitability_async(planets_df)
        
        if min_habitability > 0:
            planets_df = planets_df[planets_df['habitability_index'] >= min_habitability]
        
        if max_radius < 10:
            planets_df = planets_df[planets_df['pl_rade'] <= max_radius]
        
        if discovery_method:
            planets_df = planets_df[planets_df['discoverymethod'] == discovery_method]
        
        planets_df = planets_df.sort_values('habitability_index', ascending=False)
        
        total = len(planets_df)
        start = (page - 1) * per_page
        end = start + per_page
        
        planets = planets_df.iloc[start:end].to_dict('records')
        
        pagination = {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
        
        all_planets_df = await load_planets_async()
        discovery_methods = sorted(all_planets_df['discoverymethod'].dropna().unique().tolist())
        
        return render_template('planets.html', 
                             planets=planets, 
                             error=None, 
                             pagination=pagination,
                             discovery_methods=discovery_methods,
                             current_filters=current_filters)
    
    except Exception as e:
        import traceback
        print(f"Помилка у planets_list: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        safe_filters = {
            'min_habitability': request.args.get('min_habitability', 0, type=float),
            'max_radius': request.args.get('max_radius', 10, type=float),
            'discovery_method': request.args.get('discovery_method', '')
        }
        
        return render_template('planets.html', 
                             planets=[], 
                             error=str(e), 
                             pagination=None,
                             discovery_methods=[],
                             current_filters=safe_filters)

@exoplanets_bp.route('/api/planets')
@async_route
async def api_planets():
    """
    API endpoint для отримання списку планет через AJAX (async версія)
    """
    try:
        min_habitability = request.args.get('min_habitability', 0, type=float)
        max_radius = request.args.get('max_radius', 10, type=float)
        discovery_method = request.args.get('discovery_method', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        planets_df = await load_planets_async()
        
        if planets_df is None or planets_df.empty:
            return jsonify({'error': 'Не вдалося завантажити дані'}), 500
        
        planets_df = await calculate_habitability_async(planets_df)
        
        if min_habitability > 0:
            planets_df = planets_df[planets_df['habitability_index'] >= min_habitability]
        
        if max_radius < 10:
            planets_df = planets_df[planets_df['pl_rade'] <= max_radius]
        
        if discovery_method:
            planets_df = planets_df[planets_df['discoverymethod'] == discovery_method]
        
        planets_df = planets_df.sort_values('habitability_index', ascending=False)
        
        total = len(planets_df)
        start = (page - 1) * per_page
        end = start + per_page
        
        planets = planets_df.iloc[start:end].to_dict('records')
        
        return jsonify({
            'planets': planets,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@exoplanets_bp.route('/planet/<planet_name>')
@async_route
async def planet_detail(planet_name):
    """
    Детальна інформація про конкретну планету (async версія)
    """
    try:
        planets_df = await load_planets_async()
        
        if planets_df is None:
            return render_template('planet_detail.html', 
                                 planet=None, 
                                 error="Не вдалося завантажити дані")
        
        planets_df = await calculate_habitability_async(planets_df)
        
        planet_data = planets_df[planets_df['pl_name'] == planet_name]
        
        if planet_data.empty:
            return render_template('planet_detail.html', 
                                 planet=None, 
                                 error="Планету не знайдено")
        
        planet = planet_data.iloc[0].to_dict()
        
        # Calculate components in executor
        loop = asyncio.get_event_loop()
        components = await loop.run_in_executor(executor, calculator.get_components, planet)
        
        return render_template('planet_detail.html', 
                             planet=planet, 
                             components=components, 
                             error=None)
    
    except Exception as e:
        return render_template('planet_detail.html', 
                             planet=None, 
                             error=str(e))

@exoplanets_bp.route('/search')
@async_route
async def search():
    """
    Пошук планет за назвою (async версія)
    """
    query = request.args.get('q', '')
    
    if not query:
        return jsonify([])
    
    try:
        planets_df = await load_planets_async()
        
        mask = planets_df['pl_name'].str.contains(query, case=False, na=False) | \
               planets_df['hostname'].str.contains(query, case=False, na=False)
        
        results = planets_df[mask][['pl_name', 'hostname']].head(10)
        
        return jsonify(results.to_dict('records'))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
