import os
import sys
import tkinter as tk
from tkinter import Toplevel, Label, Frame, Button, ttk


def resource_path(relative_path):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


ICON_PATH = os.path.join(resource_path(""), "icon.ico")


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"+{x}+{y}")


def show_about():
    about_window = Toplevel()
    about_window.title("О программе")
    about_window.withdraw()
    if os.path.exists(ICON_PATH):
        about_window.iconbitmap(ICON_PATH)
    about_window.minsize(600, 400)
    # Сетка
    about_window.grid_rowconfigure(0, weight=0)
    about_window.grid_rowconfigure(1, weight=1)
    about_window.grid_rowconfigure(2, weight=0)
    about_window.grid_columnconfigure(0, weight=1)
    # Заголовок
    header_frame = Frame(about_window, bg="#2C5F8A")
    header_frame.grid(row=0, column=0, sticky="ew")
    Label(
        header_frame,
        text="Хромоматематическое моделирование",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#2C5F8A",
        padx=10,
        pady=10,
    ).pack(fill="x")
    # Информация
    info_frame = Frame(about_window, bg="#F0F8FF")
    info_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
    info_frame.grid_rowconfigure(0, weight=1)
    info_frame.grid_columnconfigure(0, weight=1)
    info_text = """Программа для хромоматематического моделирования

Особенности:
- Моделирование последовательности кубов
- Визуализация Ker-функции для суммы квадратов и кубов

Разработчик: Судовский А.Л.
Москва, 2025
"""
    text_widget = tk.Text(info_frame, wrap="word", bg="#F0F8FF", font=("Arial", 11))
    text_widget.insert("1.0", info_text)
    text_widget.config(state="disabled")
    text_widget.grid(row=0, column=0, sticky="nsew")
    # Контактная информация
    contact_frame = Frame(about_window, bg="#E1ECF4", padx=10, pady=10)
    contact_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
    Label(
        contact_frame,
        text="Контакты:  | Руководитель: Цвырко О.Л.",
        font=("Arial", 9),
        fg="#2C5F8A",
        bg="#E1ECF4",
    ).pack(fill="x")
    close_btn = Button(
        about_window,
        text="Закрыть",
        command=about_window.destroy,
        font=("Arial", 10),
        width=12,
        bg="#4A7B9D",
        fg="white",
        relief="flat",
    )
    close_btn.grid(row=3, column=0, pady=(0, 10))
    about_window.deiconify()
    center_window(about_window)
    about_window.grab_set()
    about_window.wait_window()


def show_help():
    help_window = Toplevel()
    help_window.title("Справка")
    help_window.withdraw()
    if os.path.exists(ICON_PATH):
        help_window.iconbitmap(ICON_PATH)
    help_window.minsize(500, 400)
    # Сетка
    help_window.grid_rowconfigure(0, weight=1)
    help_window.grid_columnconfigure(0, weight=1)
    help_window.configure(bg="#F0F8FF")
    # Вкладки
    tab_control = ttk.Notebook(help_window)
    tab_control.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    tab_control.grid_rowconfigure(0, weight=1)
    tab_control.grid_columnconfigure(0, weight=1)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Общая информация")
    tab_control.add(tab2, text="Функции моделирования")
    # Содержимое вкладки 1
    help_text1 = """Хромоматематическое моделирование - программа для исследования числовых закономерностей методом хромоматематики.

Основные возможности:
1. Моделирование последовательности кубов (1D)
   - Визуализация в виде столбцов
   - Спиральное представление

2. Моделирование Ker-функции для суммы квадратов и кубов (2D)
   - Цветовое кодирование значений
   - Настройка параметров отображения

Управление:
- F1: Открыть справку
- Ctrl+F1: О программе
"""
    tab1.grid_rowconfigure(0, weight=1)
    tab1.grid_columnconfigure(0, weight=1)
    Label(
        tab1, text=help_text1, justify="left", font=("Arial", 10), wraplength=450
    ).grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    # Содержимое вкладки 2
    help_text2 = """Хромоматематические модели:

1. Для кубов (1D):
   - HMM_Grad: Радужная градиентная модель
   - HMM_ModN: Дискретное представление по модулю N

2. Для Ker-функции (2D):
   - HMM_Ker: Цветовое кодирование значений Ker
   - HMM_ModN: Дискретное представление по модулю N

Ker-функция:
   Ker(n) - рекурсивная сумма цифр числа до получения
   однозначного результата.
   Пример: Ker(38) = 3+8=11 → 1+1=2
"""
    tab2.grid_rowconfigure(0, weight=1)
    tab2.grid_columnconfigure(0, weight=1)
    Label(
        tab2, text=help_text2, justify="left", font=("Arial", 10), wraplength=450
    ).grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    close_btn = Button(
        help_window,
        text="Закрыть",
        command=help_window.destroy,
        font=("Arial", 10),
        width=12,
        bg="#4A7B9D",
        fg="white",
        relief="flat",
    )
    close_btn.grid(row=1, column=0, pady=(0, 10))
    help_window.deiconify()
    center_window(help_window)
    help_window.grab_set()
    help_window.wait_window()
