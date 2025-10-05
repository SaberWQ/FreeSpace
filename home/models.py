# -*- coding: utf-8 -*-
"""
Моделі даних для модуля home
Визначає структури даних для головної сторінки
"""

# Імпорт бібліотеки для роботи з датою та часом
from datetime import datetime

class PageView:
    """
    Модель для відстеження переглядів сторінок
    Зберігає статистику відвідувань
    """
    
    def __init__(self, page_name, user_ip=None):
        """
        Ініціалізація перегляду сторінки
        
        Параметри:
            page_name (str): Назва сторінки
            user_ip (str): IP адреса користувача
        """
        # Назва сторінки
        self.page_name = page_name
        # IP адреса відвідувача
        self.user_ip = user_ip
        # Час перегляду
        self.timestamp = datetime.now()
    
    def to_dict(self):
        """
        Конвертує об'єкт у словник
        
        Повертає:
            dict: Словник з даними перегляду
        """
        return {
            'page_name': self.page_name,
            'user_ip': self.user_ip,
            'timestamp': self.timestamp.isoformat()
        }
