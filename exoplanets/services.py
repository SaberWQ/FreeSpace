# -*- coding: utf-8 -*-
"""
Сервіси для роботи з даними екзопланет
Відповідає за завантаження та кешування даних з NASA API
"""

# Імпорт бібліотеки для роботи з даними у вигляді таблиць
import pandas as pd
# Імпорт бібліотеки для HTTP запитів
import requests
# Імпорт модулів для роботи з датою та часом
from datetime import datetime, timedelta
# Імпорт модуля для роботи з файловою системою
import os
# Імпорт налаштувань проекту
from Project.settings import Config

class ExoplanetService:
    """
    Сервіс для роботи з даними екзопланет
    Завантажує дані з NASA Exoplanet Archive та кешує їх локально
    """
    
    def __init__(self):
        """
        Ініціалізація сервісу
        Встановлює параметри підключення до API та кешування
        """
        # URL API NASA Exoplanet Archive
        self.api_url = Config.EXOPLANET_API_URL
        # Шлях до файлу кешу
        self.cache_file = Config.DATA_CACHE_FILE
        # Час життя кешу в секундах
        self.cache_timeout = Config.CACHE_TIMEOUT
    
    def get_planets_data(self, force_refresh=False):
        """
        Отримує дані про екзопланети з кешу або API
        
        Параметри:
            force_refresh (bool): Якщо True - примусово оновлює дані з API
        
        Повертає:
            DataFrame: Таблиця з даними про планети або None у разі помилки
        """
        
        # Перевіряємо чи потрібно використовувати кеш
        if not force_refresh and os.path.exists(self.cache_file):
            # Отримуємо час останньої модифікації файлу кешу
            cache_age = datetime.now() - datetime.fromtimestamp(
                os.path.getmtime(self.cache_file)
            )
            
            # Якщо кеш ще актуальний - завантажуємо з нього
            if cache_age < timedelta(seconds=self.cache_timeout):
                print("✓ Завантаження даних з кешу...")
                return pd.read_csv(self.cache_file)
        
        # Якщо кеш застарів або не існує - завантажуємо з API
        print("⟳ Завантаження даних з NASA Exoplanet Archive...")
        try:
            # SQL запит для отримання даних про планети
            query = """
            SELECT 
                pl_name, hostname, discoverymethod, disc_year, disc_facility,
                pl_rade, pl_radeerr1, pl_radeerr2,
                pl_masse, pl_masseerr1, pl_masseerr2,
                pl_orbper, pl_orbpererr1, pl_orbpererr2,
                pl_orbeccen, pl_orbeccenerr1, pl_orbeccenerr2,
                pl_eqt, pl_eqterr1, pl_eqterr2,
                pl_insol, pl_insolerr1, pl_insolerr2,
                st_teff, st_tefferr1, st_tefferr2,
                st_rad, st_raderr1, st_raderr2,
                st_mass, st_masserr1, st_masserr2,
                sy_dist, sy_disterr1, sy_disterr2,
                sy_snum, sy_pnum,
                default_flag
            FROM ps
            WHERE default_flag = 1
            """
            
            # Параметри запиту до API
            params = {
                'query': query,  # SQL запит
                'format': 'csv'  # Формат відповіді - CSV
            }
            
            # Виконуємо HTTP GET запит до API
            # timeout=60 - максимальний час очікування 60 секунд
            response = requests.get(self.api_url, params=params, timeout=60)
            # Перевіряємо чи запит успішний (код 200)
            response.raise_for_status()
            
            # Створюємо директорію для кешу якщо вона не існує
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            # Зберігаємо отримані дані у файл кешу
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Завантажуємо дані з файлу у DataFrame
            df = pd.read_csv(self.cache_file)
            
            # Виводимо інформацію про кількість завантажених планет
            print(f"✓ Завантажено {len(df)} планет")
            return df
        
        except Exception as e:
            # У разі помилки виводимо повідомлення
            print(f"✗ Помилка завантаження даних: {e}")
            
            # Спробуємо завантажити застарілі дані з кешу
            if os.path.exists(self.cache_file):
                print("⚠ Використання застарілого кешу...")
                return pd.read_csv(self.cache_file)
            
            # Якщо кеш не існує - повертаємо None
            return None
