import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'exoplanet-habitability-secret-key'
    
    # NASA Exoplanet Archive API
    EXOPLANET_API_URL = 'https://exoplanetarchive.ipac.caltech.edu/TAP/sync'
    
    # Кешування даних
    CACHE_TIMEOUT = 3600  # 1 година
    DATA_CACHE_FILE = 'data/exoplanets_cache.csv'
    
    # Параметри для індексу придатності
    HABITABILITY_WEIGHTS = {
        'radius': 0.20,      # Радіус планети
        'mass': 0.15,        # Маса планети
        'temperature': 0.25, # Температура
        'stellar_flux': 0.15,# Коефіцієнт світлового потоку
        'orbital_period': 0.10, # Орбітальний період
        'eccentricity': 0.10,   # Ексцентриситет орбіти
        'distance': 0.05     # Відстань від Землі
    }
    
    # Оптимальні діапазони для життя
    OPTIMAL_RANGES = {
        'radius': {'optimal': 1.0, 'min': 0.5, 'max': 2.5},
        'mass': {'optimal': 1.0, 'min': 0.3, 'max': 3.0},
        'temperature': {'optimal': 288, 'min': 200, 'max': 350},
        'stellar_flux': {'optimal': 1.0, 'min': 0.5, 'max': 1.5},
        'orbital_period': {'optimal': 365, 'min': 100, 'max': 700},
        'eccentricity': {'optimal': 0.0, 'min': 0.0, 'max': 0.5},
        'distance': {'optimal': 0, 'min': 0, 'max': 1000}
    }
