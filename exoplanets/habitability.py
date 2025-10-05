# -*- coding: utf-8 -*-
"""
Калькулятор індексу придатності екзопланет
Розраховує наскільки планета придатна для життя
"""

# Імпорт бібліотеки для числових обчислень
import numpy as np
# Імпорт бібліотеки для роботи з даними
import pandas as pd
# Імпорт налаштувань проекту
from Project.settings import Config

class HabitabilityCalculator:
    """
    Клас для розрахунку індексу придатності планет до життя
    Базується на порівнянні параметрів планети з оптимальними значеннями
    """
    
    def __init__(self):
        """
        Ініціалізація калькулятора
        Завантажує ваги та оптимальні діапазони з конфігурації
        """
        # Ваги для кожного параметра (сума = 1.0)
        self.weights = Config.HABITABILITY_WEIGHTS
        # Оптимальні діапазони для кожного параметра
        self.optimal_ranges = Config.OPTIMAL_RANGES
    
    def calculate_parameter_score(self, value, param_name):
        """
        Розраховує оцінку для одного параметра
        
        Параметри:
            value (float): Значення параметра
            param_name (str): Назва параметра
        
        Повертає:
            float: Оцінка від 0 до 100
        """
        # Якщо значення відсутнє - повертаємо 0
        if pd.isna(value):
            return 0.0
        
        # Отримуємо оптимальні діапазони для параметра
        ranges = self.optimal_ranges.get(param_name)
        # Якщо діапазони не визначені - повертаємо 0
        if not ranges:
            return 0.0
        
        # Отримуємо оптимальне, мінімальне та максимальне значення
        optimal = ranges['optimal']
        min_val = ranges['min']
        max_val = ranges['max']
        
        # Якщо значення поза допустимим діапазоном - повертаємо 0
        if value < min_val or value > max_val:
            return 0.0
        
        # Якщо діапазон вироджений (min == optimal == max) - повертаємо 100
        if min_val == max_val:
            return 100.0 if value == optimal else 0.0
        
        # Розраховуємо відхилення від оптимального значення
        if value <= optimal:
            # Якщо значення менше оптимального
            # Нормалізуємо в діапазоні [min_val, optimal]
            if optimal == min_val:
                score = 100.0
            else:
                score = ((value - min_val) / (optimal - min_val)) * 100
        else:
            # Якщо значення більше оптимального
            # Нормалізуємо в діапазоні [optimal, max_val]
            if max_val == optimal:
                score = 100.0
            else:
                score = ((max_val - value) / (max_val - optimal)) * 100
        
        # Обмежуємо оцінку діапазоном [0, 100]
        return max(0.0, min(100.0, score))
    
    def calculate_habitability_index(self, planet_data):
        """
        Розраховує загальний індекс придатності планети
        
        Параметри:
            planet_data (dict): Словник з параметрами планети
        
        Повертає:
            float: Індекс придатності від 0 до 100
        """
        # Ініціалізуємо загальну оцінку
        total_score = 0.0
        # Лічильник врахованих параметрів
        total_weight = 0.0
        
        # Відповідність назв параметрів у даних та конфігурації
        param_mapping = {
            'radius': 'pl_rade',        # Радіус планети
            'mass': 'pl_masse',         # Маса планети
            'temperature': 'pl_eqt',    # Температура
            'stellar_flux': 'pl_insol', # Світловий потік
            'orbital_period': 'pl_orbper',  # Орбітальний період
            'eccentricity': 'pl_orbeccen',  # Ексцентриситет
            'distance': 'sy_dist'       # Відстань від Землі
        }
        
        # Проходимо по всіх параметрах
        for param_name, data_key in param_mapping.items():
            # Отримуємо значення параметра з даних
            value = planet_data.get(data_key)
            # Якщо значення існує
            if value is not None and not pd.isna(value):
                # Розраховуємо оцінку для параметра
                score = self.calculate_parameter_score(value, param_name)
                # Отримуємо вагу параметра
                weight = self.weights.get(param_name, 0)
                # Додаємо зважену оцінку до загальної
                total_score += score * weight
                # Додаємо вагу до загальної ваги
                total_weight += weight
        
        # Якщо жоден параметр не врахований - повертаємо 0
        if total_weight == 0:
            return 0.0
        
        # Нормалізуємо оцінку відносно врахованих ваг
        normalized_score = total_score / total_weight
        
        # Повертаємо індекс придатності
        return round(normalized_score, 2)
    
    def calculate_batch(self, planets_df):
        """
        Розраховує індекс придатності для всіх планет у DataFrame
        
        Параметри:
            planets_df (DataFrame): Таблиця з даними про планети
        
        Повертає:
            DataFrame: Таблиця з доданою колонкою habitability_index
        """
        # Створюємо копію DataFrame щоб не змінювати оригінал
        df = planets_df.copy()
        
        # Застосовуємо функцію розрахунку до кожного рядка
        # axis=1 означає що функція застосовується до рядків
        df['habitability_index'] = df.apply(
            lambda row: self.calculate_habitability_index(row.to_dict()),
            axis=1
        )
        
        # Повертаємо оновлений DataFrame
        return df
    
    def get_components(self, planet_data):
        """
        Отримує детальні компоненти індексу придатності
        
        Параметри:
            planet_data (dict): Словник з параметрами планети
        
        Повертає:
            dict: Словник з оцінками для кожного параметра
        """
        # Словник для збереження компонентів
        components = {}
        
        # Відповідність назв параметрів
        param_mapping = {
            'radius': ('pl_rade', 'Радіус'),
            'mass': ('pl_masse', 'Маса'),
            'temperature': ('pl_eqt', 'Температура'),
            'stellar_flux': ('pl_insol', 'Світловий потік'),
            'orbital_period': ('pl_orbper', 'Орбітальний період'),
            'eccentricity': ('pl_orbeccen', 'Ексцентриситет'),
            'distance': ('sy_dist', 'Відстань')
        }
        
        # Розраховуємо оцінку для кожного параметра
        for param_name, (data_key, display_name) in param_mapping.items():
            # Отримуємо значення параметра
            value = planet_data.get(data_key)
            # Розраховуємо оцінку
            score = self.calculate_parameter_score(value, param_name)
            # Отримуємо вагу параметра
            weight = self.weights.get(param_name, 0)
            
            # Зберігаємо компонент
            components[param_name] = {
                'name': display_name,      # Відображувана назва
                'value': value,            # Значення параметра
                'score': score,            # Оцінка (0-100)
                'weight': weight * 100,    # Вага у відсотках
                'contribution': score * weight  # Внесок у загальний індекс
            }
        
        # Повертаємо словник з компонентами
        return components
