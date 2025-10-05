# -*- coding: utf-8 -*-
"""
Конфігурація додатку exoplanets
Містить налаштування для роботи з екзопланетами
"""

class ExoplanetsConfig:
    """
    Клас конфігурації для додатку exoplanets
    Визначає основні параметри модуля
    """
    
    # Назва додатку
    name = 'exoplanets'
    
    # Відображувана назва
    verbose_name = 'Екзопланети'
    
    # Шлях до шаблонів
    template_folder = 'templates/exoplanets'
    
    # Шлях до статичних файлів
    static_folder = 'static/exoplanets'
