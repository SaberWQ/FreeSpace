# -*- coding: utf-8 -*-
"""
Моделі даних для користувачів
Визначає структури даних для користувачів системи
"""

# Імпорт бібліотеки для роботи з датою та часом
from datetime import datetime

class User:
    """
    Модель користувача системи
    Базовий клас для майбутнього розширення функціоналу
    """
    
    def __init__(self, username, email):
        """
        Ініціалізація користувача
        
        Параметри:
            username (str): Ім'я користувача
            email (str): Email адреса
        """
        # Унікальний ідентифікатор (буде генеруватись автоматично)
        self.id = None
        # Ім'я користувача
        self.username = username
        # Email адреса
        self.email = email
        # Дата створення акаунту
        self.created_at = datetime.now()
        # Дата останнього входу
        self.last_login = None
        # Чи активний акаунт
        self.is_active = True
    
    def to_dict(self):
        """
        Конвертує об'єкт користувача у словник
        
        Повертає:
            dict: Словник з даними користувача
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
