# -*- coding: utf-8 -*-
"""
Моделі даних для екзопланет
Визначає структури даних для планет та їх параметрів
"""

# Імпорт бібліотеки для роботи з даними
import pandas as pd
# Імпорт бібліотеки для числових обчислень
import numpy as np

class Exoplanet:
    """
    Модель екзопланети
    Представляє одну екзопланету з усіма її параметрами
    """
    
    def __init__(self, data_dict):
        """
        Ініціалізація екзопланети з даних
        
        Параметри:
            data_dict (dict): Словник з параметрами планети
        """
        # Назва планети
        self.name = data_dict.get('pl_name', 'Unknown')
        # Назва зірки-господаря
        self.hostname = data_dict.get('hostname', 'Unknown')
        # Метод відкриття
        self.discovery_method = data_dict.get('discoverymethod', 'Unknown')
        # Рік відкриття
        self.discovery_year = data_dict.get('disc_year', None)
        
        # Фізичні параметри планети
        self.radius = data_dict.get('pl_rade', None)  # Радіус (в радіусах Землі)
        self.mass = data_dict.get('pl_masse', None)    # Маса (в масах Землі)
        
        # Орбітальні параметри
        self.orbital_period = data_dict.get('pl_orbper', None)  # Період обертання (дні)
        self.eccentricity = data_dict.get('pl_orbeccen', None)  # Ексцентриситет орбіти
        
        # Температурні параметри
        self.equilibrium_temp = data_dict.get('pl_eqt', None)  # Рівноважна температура (K)
        self.stellar_flux = data_dict.get('pl_insol', None)    # Світловий потік
        
        # Параметри зірки
        self.stellar_temp = data_dict.get('st_teff', None)     # Температура зірки (K)
        self.stellar_radius = data_dict.get('st_rad', None)    # Радіус зірки
        self.stellar_mass = data_dict.get('st_mass', None)     # Маса зірки
        
        # Відстань від Землі
        self.distance = data_dict.get('sy_dist', None)  # Відстань (парсеки)
        
        # Індекс придатності (розраховується окремо)
        self.habitability_index = data_dict.get('habitability_index', 0)
    
    def to_dict(self):
        """
        Конвертує об'єкт планети у словник
        
        Повертає:
            dict: Словник з усіма параметрами планети
        """
        return {
            'name': self.name,
            'hostname': self.hostname,
            'discovery_method': self.discovery_method,
            'discovery_year': self.discovery_year,
            'radius': self.radius,
            'mass': self.mass,
            'orbital_period': self.orbital_period,
            'eccentricity': self.eccentricity,
            'equilibrium_temp': self.equilibrium_temp,
            'stellar_flux': self.stellar_flux,
            'stellar_temp': self.stellar_temp,
            'stellar_radius': self.stellar_radius,
            'stellar_mass': self.stellar_mass,
            'distance': self.distance,
            'habitability_index': self.habitability_index
        }
    
    def is_potentially_habitable(self, threshold=50):
        """
        Перевіряє чи планета потенційно придатна для життя
        
        Параметри:
            threshold (float): Мінімальний індекс придатності
            
        Повертає:
            bool: True якщо планета придатна, False якщо ні
        """
        # Порівнюємо індекс придатності з порогом
        return self.habitability_index >= threshold
