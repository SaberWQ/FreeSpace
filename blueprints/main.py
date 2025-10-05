from flask import Blueprint, render_template, request, jsonify
from services.exoplanet_service import ExoplanetService
from services.habitability_calculator import HabitabilityCalculator

main_bp = Blueprint('main', __name__)
exoplanet_service = ExoplanetService()
calculator = HabitabilityCalculator()

@main_bp.route('/')
def index():
    """Головна сторінка"""
    return render_template('index.html')

@main_bp.route('/planets')
def planets_list():
    """Список екзопланет з індексом придатності"""
    try:
        # Отримання параметрів фільтрації
        min_habitability = request.args.get('min_habitability', 0, type=float)
        max_radius = request.args.get('max_radius', 10, type=float)
        discovery_method = request.args.get('discovery_method', '')
        page = request.args.get('page', 1, type=int)
        per_page = 50
        
        # Завантаження даних
        planets_df = exoplanet_service.get_planets_data()
        
        if planets_df is None or planets_df.empty:
            return render_template('planets.html', planets=[], error="Не вдалося завантажити дані", pagination=None)
        
        # Розрахунок індексу придатності
        planets_df = calculator.calculate_batch(planets_df)
        
        # Фільтрація
        if min_habitability > 0:
            planets_df = planets_df[planets_df['habitability_index'] >= min_habitability]
        
        if max_radius < 10:
            planets_df = planets_df[planets_df['pl_rade'] <= max_radius]
        
        if discovery_method:
            planets_df = planets_df[planets_df['discoverymethod'] == discovery_method]
        
        # Сортування за індексом
        planets_df = planets_df.sort_values('habitability_index', ascending=False)
        
        # Пагінація
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
        
        # Отримання методів відкриття для фільтра
        discovery_methods = planets_df['discoverymethod'].unique().tolist()
        
        return render_template('planets.html', 
                             planets=planets, 
                             error=None, 
                             pagination=pagination,
                             discovery_methods=discovery_methods,
                             current_filters={
                                 'min_habitability': min_habitability,
                                 'max_radius': max_radius,
                                 'discovery_method': discovery_method
                             })
    
    except Exception as e:
        return render_template('planets.html', planets=[], error=str(e), pagination=None)

@main_bp.route('/planet/<planet_name>')
def planet_detail(planet_name):
    """Детальна інформація про планету"""
    try:
        planets_df = exoplanet_service.get_planets_data()
        
        if planets_df is None:
            return render_template('planet_detail.html', planet=None, error="Не вдалося завантажити дані")
        
        # Розрахунок індексу
        planets_df = calculator.calculate_batch(planets_df)
        
        # Пошук планети
        planet_data = planets_df[planets_df['pl_name'] == planet_name]
        
        if planet_data.empty:
            return render_template('planet_detail.html', planet=None, error="Планету не знайдено")
        
        planet = planet_data.iloc[0].to_dict()
        
        # Розрахунок детального індексу з компонентами
        components = calculator.get_components(planet)
        
        return render_template('planet_detail.html', planet=planet, components=components, error=None)
    
    except Exception as e:
        return render_template('planet_detail.html', planet=None, error=str(e))

@main_bp.route('/search')
def search():
    """Пошук планет"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify([])
    
    try:
        planets_df = exoplanet_service.get_planets_data()
        
        # Пошук за назвою планети або зірки
        mask = planets_df['pl_name'].str.contains(query, case=False, na=False) | \
               planets_df['hostname'].str.contains(query, case=False, na=False)
        
        results = planets_df[mask][['pl_name', 'hostname']].head(10)
        
        return jsonify(results.to_dict('records'))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
