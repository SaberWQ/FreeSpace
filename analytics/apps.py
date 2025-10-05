# -*- coding: utf-8 -*-
"""
Конфігурація додатку analytics
Містить налаштування для аналітики
"""

class AnalyticsConfig:
    """
    Клас конфігурації для додатку analytics
    Визначає основні параметри модуля
    """
    
    # Назва додатку
    name = 'analytics'
    
    # Відображувана назва
    verbose_name = 'Аналітика'
    
    # Шлях до шаблонів
    template_folder = 'templates/analytics'
    
    # Шлях до статичних файлів
    static_folder = 'static/analytics'
