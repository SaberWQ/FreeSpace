# -*- coding: utf-8 -*-
"""
Views (представлення) для модуля user
Обробляє запити для роботи з користувачами
"""

# Імпорт необхідних компонентів Flask
from flask import Blueprint, render_template, jsonify

# Створюємо Blueprint для модуля user
user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
def profile():
    """
    Профіль користувача
    
    Маршрут: /user/profile
    Метод: GET
    
    Повертає:
        HTML: Сторінка профілю користувача
    """
    # Заглушка для майбутнього функціоналу
    return render_template('user/profile.html')
