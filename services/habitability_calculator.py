import pandas as pd
import numpy as np
from config import Config

class HabitabilityCalculator:
    def __init__(self):
        self.weights = Config.HABITABILITY_WEIGHTS
        self.optimal_ranges = Config.OPTIMAL_RANGES
    
    def normalize_value(self, value, optimal, min_val, max_val):
        """Нормалізація значення відносно оптимального діапазону"""
        if pd.isna(value):
            return 0.0
        
        if value < min_val or value > max_val:
            return 0.0
        
        distance = abs(value - optimal)
        max_distance = max(abs(optimal - min_val), abs(optimal - max_val))
        
        if max_distance == 0.0:
            return 1.0
        
        score = 1.0 - (distance / max_distance)
        return max(0.0, min(1.0, score))
    
    def calculate_radius_score(self, radius):
        """Оцінка радіусу планети"""
        params = self.optimal_ranges['radius']
        return self.normalize_value(radius, params['optimal'], params['min'], params['max'])
    
    def calculate_mass_score(self, mass):
        """Оцінка маси планети"""
        params = self.optimal_ranges['mass']
        return self.normalize_value(mass, params['optimal'], params['min'], params['max'])
    
    def calculate_temperature_score(self, temperature):
        """Оцінка температури"""
        params = self.optimal_ranges['temperature']
        return self.normalize_value(temperature, params['optimal'], params['min'], params['max'])
    
    def calculate_stellar_flux_score(self, insol):
        """Оцінка світлового потоку"""
        params = self.optimal_ranges['stellar_flux']
        return self.normalize_value(insol, params['optimal'], params['min'], params['max'])
    
    def calculate_orbital_period_score(self, period):
        """Оцінка орбітального періоду"""
        params = self.optimal_ranges['orbital_period']
        return self.normalize_value(period, params['optimal'], params['min'], params['max'])
    
    def calculate_eccentricity_score(self, eccentricity):
        """Оцінка ексцентриситету"""
        if pd.isna(eccentricity):
            return 0.5
        return max(0.0, 1.0 - eccentricity)
    
    def calculate_distance_score(self, distance):
        """Оцінка відстані від Землі"""
        if pd.isna(distance):
            return 0.0
        
        if distance <= 100.0:
            return 1.0
        elif distance >= 1000.0:
            return 0.1
        else:
            return 1.0 - ((distance - 100.0) / 900.0) * 0.9
    
    def calculate_single(self, planet_data):
        """Розрахунок індексу для однієї планети"""
        score_radius = self.calculate_radius_score(planet_data.get('pl_rade', np.nan))
        score_mass = self.calculate_mass_score(planet_data.get('pl_masse', np.nan))
        score_temp = self.calculate_temperature_score(planet_data.get('pl_eqt', np.nan))
        score_flux = self.calculate_stellar_flux_score(planet_data.get('pl_insol', np.nan))
        score_period = self.calculate_orbital_period_score(planet_data.get('pl_orbper', np.nan))
        score_ecc = self.calculate_eccentricity_score(planet_data.get('pl_orbeccen', np.nan))
        score_dist = self.calculate_distance_score(planet_data.get('sy_dist', np.nan))
        
        habitability_index = (
            score_radius * self.weights['radius'] +
            score_mass * self.weights['mass'] +
            score_temp * self.weights['temperature'] +
            score_flux * self.weights['stellar_flux'] +
            score_period * self.weights['orbital_period'] +
            score_ecc * self.weights['eccentricity'] +
            score_dist * self.weights['distance']
        ) * 100.0
        
        return habitability_index
    
    def calculate_batch(self, planets_df):
        """Векторизований розрахунок для DataFrame"""
        # Розрахунок окремих компонентів
        planets_df['score_radius'] = planets_df['pl_rade'].apply(self.calculate_radius_score)
        planets_df['score_mass'] = planets_df['pl_masse'].apply(self.calculate_mass_score)
        planets_df['score_temperature'] = planets_df['pl_eqt'].apply(self.calculate_temperature_score)
        planets_df['score_stellar_flux'] = planets_df['pl_insol'].apply(self.calculate_stellar_flux_score)
        planets_df['score_orbital_period'] = planets_df['pl_orbper'].apply(self.calculate_orbital_period_score)
        planets_df['score_eccentricity'] = planets_df['pl_orbeccen'].apply(self.calculate_eccentricity_score)
        planets_df['score_distance'] = planets_df['sy_dist'].apply(self.calculate_distance_score)
        
        # Розрахунок загального індексу
        planets_df['habitability_index'] = (
            planets_df['score_radius'] * self.weights['radius'] +
            planets_df['score_mass'] * self.weights['mass'] +
            planets_df['score_temperature'] * self.weights['temperature'] +
            planets_df['score_stellar_flux'] * self.weights['stellar_flux'] +
            planets_df['score_orbital_period'] * self.weights['orbital_period'] +
            planets_df['score_eccentricity'] * self.weights['eccentricity'] +
            planets_df['score_distance'] * self.weights['distance']
        ) * 100.0
        
        return planets_df
    
    def get_components(self, planet):
        """Отримання детальних компонентів індексу"""
        components = {
            'radius': {
                'value': planet.get('pl_rade'),
                'score': self.calculate_radius_score(planet.get('pl_rade', np.nan)),
                'weight': self.weights['radius']
            },
            'mass': {
                'value': planet.get('pl_masse'),
                'score': self.calculate_mass_score(planet.get('pl_masse', np.nan)),
                'weight': self.weights['mass']
            },
            'temperature': {
                'value': planet.get('pl_eqt'),
                'score': self.calculate_temperature_score(planet.get('pl_eqt', np.nan)),
                'weight': self.weights['temperature']
            },
            'stellar_flux': {
                'value': planet.get('pl_insol'),
                'score': self.calculate_stellar_flux_score(planet.get('pl_insol', np.nan)),
                'weight': self.weights['stellar_flux']
            },
            'orbital_period': {
                'value': planet.get('pl_orbper'),
                'score': self.calculate_orbital_period_score(planet.get('pl_orbper', np.nan)),
                'weight': self.weights['orbital_period']
            },
            'eccentricity': {
                'value': planet.get('pl_orbeccen'),
                'score': self.calculate_eccentricity_score(planet.get('pl_orbeccen', np.nan)),
                'weight': self.weights['eccentricity']
            },
            'distance': {
                'value': planet.get('sy_dist'),
                'score': self.calculate_distance_score(planet.get('sy_dist', np.nan)),
                'weight': self.weights['distance']
            }
        }
        
        return components
