import pandas as pd
import numpy as np

class AnalyticsService:
    
    def get_habitability_distribution(self, planets_df):
        """Розподіл індексу придатності"""
        bins = [0, 20, 40, 60, 80, 100]
        labels = ['Дуже низька (0-20)', 'Низька (20-40)', 'Середня (40-60)', 'Висока (60-80)', 'Дуже висока (80-100)']
        
        planets_df['habitability_category'] = pd.cut(
            planets_df['habitability_index'],
            bins=bins,
            labels=labels,
            include_lowest=True
        )
        
        distribution = planets_df['habitability_category'].value_counts().sort_index().to_dict()
        
        return {
            'labels': labels,
            'values': [distribution.get(label, 0) for label in labels],
            'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6']
        }
    
    def get_parameters_correlation(self, planets_df):
        """Кореляція між параметрами та індексом придатності"""
        params = {
            'pl_rade': 'Радіус',
            'pl_masse': 'Маса',
            'pl_eqt': 'Температура',
            'pl_insol': 'Світловий потік',
            'pl_orbper': 'Орбітальний період',
            'pl_orbeccen': 'Ексцентриситет'
        }
        
        correlations = {}
        labels = []
        values = []
        
        for param, label in params.items():
            if param in planets_df.columns:
                corr = planets_df[['habitability_index', param]].corr().iloc[0, 1]
                if not pd.isna(corr):
                    correlations[label] = float(corr)
                    labels.append(label)
                    values.append(float(corr))
        
        return {
            'labels': labels,
            'values': values,
            'correlations': correlations
        }
    
    def get_discovery_timeline(self, planets_df):
        """Часова шкала відкриттів планет"""
        timeline_df = planets_df.dropna(subset=['disc_year'])
        timeline = timeline_df.groupby('disc_year').agg({
            'pl_name': 'count',
            'habitability_index': 'mean'
        }).reset_index()
        
        timeline.columns = ['year', 'count', 'avg_habitability']
        timeline = timeline.sort_values('year')
        
        return {
            'years': [int(year) for year in timeline['year'].tolist()],
            'counts': timeline['count'].tolist(),
            'avg_habitability': [float(x) for x in timeline['avg_habitability'].tolist()]
        }
    
    def get_top_habitable_planets(self, planets_df, top_n=20):
        """Топ найпридатніших планет"""
        top_planets = planets_df.nlargest(top_n, 'habitability_index')
        
        return {
            'names': top_planets['pl_name'].tolist(),
            'indices': [float(x) for x in top_planets['habitability_index'].tolist()],
            'radii': [float(x) if not pd.isna(x) else None for x in top_planets['pl_rade'].tolist()],
            'temperatures': [float(x) if not pd.isna(x) else None for x in top_planets['pl_eqt'].tolist()],
            'methods': top_planets['discoverymethod'].tolist()
        }
    
    def get_discovery_method_comparison(self, planets_df):
        """Порівняння методів відкриття"""
        method_stats = planets_df.groupby('discoverymethod').agg({
            'pl_name': 'count',
            'habitability_index': ['mean', 'max', 'std']
        }).reset_index()
        
        method_stats.columns = ['method', 'count', 'avg_habitability', 'max_habitability', 'std_habitability']
        method_stats = method_stats.sort_values('count', ascending=False).head(10)
        
        return {
            'methods': method_stats['method'].tolist(),
            'counts': method_stats['count'].tolist(),
            'avg_habitability': [float(x) for x in method_stats['avg_habitability'].tolist()],
            'max_habitability': [float(x) for x in method_stats['max_habitability'].tolist()]
        }
