# -*- coding: utf-8 -*-
"""
Сервіси для аналітики даних
Обробляє та агрегує дані для візуалізації
"""

# Імпорт бібліотеки для роботи з даними
import pandas as pd
# Імпорт бібліотеки для числових обчислень
import numpy as np

class AnalyticsService:
    """
    Клас для аналітичної обробки даних про екзопланети
    Генерує статистику та дані для графіків
    """
    
    def get_habitability_distribution(self, planets_df):
        """
        Розраховує розподіл планет за індексом придатності
        
        Параметри:
            planets_df (DataFrame): Таблиця з даними про планети
        
        Повертає:
            dict: Дані для побудови графіка розподілу
        """
        # Визначаємо межі категорій індексу придатності
        bins = [0, 20, 40, 60, 80, 100]
        # Назви категорій
        labels = [
            'Дуже низька (0-20)',   # Непридатні планети
            'Низька (20-40)',        # Малопридатні планети
            'Середня (40-60)',       # Помірно придатні планети
            'Висока (60-80)',        # Придатні планети
            'Дуже висока (80-100)'   # Дуже придатні планети
        ]
        
        # Розбиваємо планети на категорії
        # include_lowest=True - включаємо нижню межу
        planets_df['habitability_category'] = pd.cut(
            planets_df['habitability_index'],
            bins=bins,
            labels=labels,
            include_lowest=True
        )
        
        # Підраховуємо кількість планет у кожній категорії
        distribution = planets_df['habitability_category'].value_counts().sort_index().to_dict()
        
        # Формуємо результат для графіка
        return {
            'labels': labels,  # Назви категорій
            'values': [distribution.get(label, 0) for label in labels],  # Кількість планет
            'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6']  # Кольори для графіка
        }
    
    def get_parameters_correlation(self, planets_df):
        """
        Розраховує кореляцію між параметрами та індексом придатності
        
        Параметри:
            planets_df (DataFrame): Таблиця з даними про планети
        
        Повертає:
            dict: Дані про кореляцію параметрів
        """
        # Відповідність назв параметрів у даних та для відображення
        params = {
            'pl_rade': 'Радіус',              # Радіус планети
            'pl_masse': 'Маса',               # Маса планети
            'pl_eqt': 'Температура',          # Температура
            'pl_insol': 'Світловий потік',    # Світловий потік
            'pl_orbper': 'Орбітальний період', # Період обертання
            'pl_orbeccen': 'Ексцентриситет'   # Ексцентриситет орбіти
        }
        
        # Словники для збереження результатів
        correlations = {}
        labels = []
        values = []
        
        # Розраховуємо кореляцію для кожного параметра
        for param, label in params.items():
            # Перевіряємо чи параметр існує в даних
            if param in planets_df.columns:
                # Розраховуємо коефіцієнт кореляції Пірсона
                corr = planets_df[['habitability_index', param]].corr().iloc[0, 1]
                # Якщо кореляція розрахована успішно
                if not pd.isna(corr):
                    # Зберігаємо результати
                    correlations[label] = float(corr)
                    labels.append(label)
                    values.append(float(corr))
        
        # Повертаємо результати
        return {
            'labels': labels,           # Назви параметрів
            'values': values,           # Значення кореляції
            'correlations': correlations # Словник з кореляціями
        }
    
    def get_discovery_timeline(self, planets_df):
        """
        Створює часову шкалу відкриттів планет
        
        Параметри:
            planets_df (DataFrame): Таблиця з даними про планети
        
        Повертає:
            dict: Дані про відкриття планет по роках
        """
        # Видаляємо рядки без року відкриття
        timeline_df = planets_df.dropna(subset=['disc_year'])
        
        # Групуємо дані по роках та розраховуємо статистику
        timeline = timeline_df.groupby('disc_year').agg({
            'pl_name': 'count',                    # Кількість відкритих планет
            'habitability_index': 'mean'           # Середній індекс придатності
        }).reset_index()
        
        # Перейменовуємо колонки для зручності
        timeline.columns = ['year', 'count', 'avg_habitability']
        # Сортуємо за роком
        timeline = timeline.sort_values('year')
        
        # Формуємо результат
        return {
            'years': [int(year) for year in timeline['year'].tolist()],  # Роки
            'counts': timeline['count'].tolist(),                         # Кількість відкриттів
            'avg_habitability': [float(x) for x in timeline['avg_habitability'].tolist()]  # Середній індекс
        }
    
    def get_top_habitable_planets(self, planets_df, top_n=20):
        """
        Отримує топ найпридатніших планет
        
        Параметри:
            planets_df (DataFrame): Таблиця з даними про планети
            top_n (int): Кількість планет у топі
        
        Повертає:
            dict: Дані про топ планет
        """
        # Вибираємо топ-N планет за індексом придатності
        top_planets = planets_df.nlargest(top_n, 'habitability_index')
        
        # Формуємо результат
        return {
            'names': top_planets['pl_name'].tolist(),  # Назви планет
            'indices': [float(x) for x in top_planets['habitability_index'].tolist()],  # Індекси
            'radii': [float(x) if not pd.isna(x) else None for x in top_planets['pl_rade'].tolist()],  # Радіуси
            'temperatures': [float(x) if not pd.isna(x) else None for x in top_planets['pl_eqt'].tolist()],  # Температури
            'methods': top_planets['discoverymethod'].tolist()  # Методи відкриття
        }
    
    def get_discovery_method_comparison(self, planets_df):
        """
        Порівнює методи відкриття планет
        
        Параметри:
            planets_df (DataFrame): Таблиця з даними про планети
        
        Повертає:
            dict: Статистика по методах відкриття
        """
        # Групуємо дані по методах відкриття та розраховуємо статистику
        method_stats = planets_df.groupby('discoverymethod').agg({
            'pl_name': 'count',                      # Кількість планет
            'habitability_index': ['mean', 'max', 'std']  # Середній, макс та стандартне відхилення індексу
        }).reset_index()
        
        # Перейменовуємо колонки
        method_stats.columns = ['method', 'count', 'avg_habitability', 'max_habitability', 'std_habitability']
        # Сортуємо за кількістю відкриттів та беремо топ-10
        method_stats = method_stats.sort_values('count', ascending=False).head(10)
        
        # Формуємо результат
        return {
            'methods': method_stats['method'].tolist(),  # Назви методів
            'counts': method_stats['count'].tolist(),    # Кількість відкриттів
            'avg_habitability': [float(x) for x in method_stats['avg_habitability'].tolist()],  # Середній індекс
            'max_habitability': [float(x) for x in method_stats['max_habitability'].tolist()]   # Максимальний індекс
        }
