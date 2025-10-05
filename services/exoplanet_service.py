import pandas as pd
import requests
from datetime import datetime, timedelta
import os
from config import Config

class ExoplanetService:
    def __init__(self):
        self.api_url = Config.EXOPLANET_API_URL
        self.cache_file = Config.DATA_CACHE_FILE
        self.cache_timeout = Config.CACHE_TIMEOUT
    
    def get_planets_data(self, force_refresh=False):
        """Отримання даних про екзопланети з кешуванням"""
        
        # Перевірка кешу
        if not force_refresh and os.path.exists(self.cache_file):
            cache_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(self.cache_file))
            
            if cache_age < timedelta(seconds=self.cache_timeout):
                print("Завантаження з кешу...")
                return pd.read_csv(self.cache_file)
        
        # Завантаження з API
        print("Завантаження з NASA Exoplanet Archive...")
        try:
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
            
            params = {
                'query': query,
                'format': 'csv'
            }
            
            response = requests.get(self.api_url, params=params, timeout=60)
            response.raise_for_status()
            
            # Збереження в кеш
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Завантаження DataFrame
            df = pd.read_csv(self.cache_file)
            
            print(f"Завантажено {len(df)} планет")
            return df
        
        except Exception as e:
            print(f"Помилка завантаження даних: {e}")
            
            # Спроба завантажити з кешу
            if os.path.exists(self.cache_file):
                print("Використання застарілого кешу...")
                return pd.read_csv(self.cache_file)
            
            return None
