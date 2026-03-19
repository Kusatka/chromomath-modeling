"""Конфигурация путей для работы в режиме скрипта и exe."""
import os
import sys


def get_app_dir():
    """Папка приложения: при exe — папка с exe, иначе — папка main.py."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_data_path():
    """Путь к файлу data.txt."""
    return os.path.join(get_app_dir(), "data.txt")
