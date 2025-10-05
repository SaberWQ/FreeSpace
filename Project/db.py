# -*- coding: utf-8 -*-
"""
Модуль для роботи з базою даних
Містить функції для підключення та роботи з даними
"""

# Імпорт бібліотеки для роботи з даними у вигляді таблиць
import pandas as pd
# Імпорт модуля для роботи з файловою системою
import os

class DatabaseManager:
    """
    Клас для управління базою даних проекту
    Відповідає за збереження та завантаження даних
    """
    
    def __init__(self, data_dir='data'):
        """
        Ініціалізація менеджера бази даних
        
        Параметри:
            data_dir (str): Директорія для збереження даних
        """
        # Зберігаємо шлях до директорії з даними
        self.data_dir = data_dir
        # Створюємо директорію, якщо вона не існує
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_dataframe(self, df, filename):
        """
        Зберігає DataFrame у CSV файл
        
        Параметри:
            df (DataFrame): Таблиця даних для збереження
            filename (str): Ім'я файлу
        """
        # Формуємо повний шлях до файлу
        filepath = os.path.join(self.data_dir, filename)
        # Зберігаємо дані у CSV форматі з UTF-8 кодуванням
        df.to_csv(filepath, index=False, encoding='utf-8')
    
    def load_dataframe(self, filename):
        """
        Завантажує DataFrame з CSV файлу
        
        Параметри:
            filename (str): Ім'я файлу
            
        Повертає:
            DataFrame: Завантажені дані або None якщо файл не існує
        """
        # Формуємо повний шлях до файлу
        filepath = os.path.join(self.data_dir, filename)
        # Перевіряємо чи існує файл
        if os.path.exists(filepath):
            # Завантажуємо та повертаємо дані
            return pd.read_csv(filepath)
        # Повертаємо None якщо файл не знайдено
        return None
