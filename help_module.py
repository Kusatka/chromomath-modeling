# -*- coding: utf-8 -*-
import os
import sys
import tkinter as tk
from tkinter import Toplevel, Label, Frame, Button, ttk


def resource_path(relative_path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


ICON_PATH = resource_path("icon.ico")


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
        try:
            about_window.iconbitmap(ICON_PATH)
        except:
            pass
    about_window.minsize(600, 400)

    about_window.grid_rowconfigure(0, weight=0)
    about_window.grid_rowconfigure(1, weight=1)
    about_window.grid_rowconfigure(2, weight=0)
    about_window.grid_columnconfigure(0, weight=1)

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

    info_frame = Frame(about_window, bg="#F0F8FF")
    info_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
    info_frame.grid_rowconfigure(0, weight=1)
    info_frame.grid_columnconfigure(0, weight=1)

    info_text = """Программа для хромоматематического моделирования

Основная идея:
Числовые последовательности переводятся в цветовое представление.
Цвет и геометрия помогают увидеть закономерности и периодичность.

Особенности:
- Моделирование последовательности кубов (1D)
  * Четыре режима: столбцы и три типа спиралей
  * Оптимизация памяти для 3000 значений
  
- Визуализация Ker-функции (2D)
  * Исследование суммы квадратов и кубов
  * Две цветовые модели

- Плавная работа даже на слабых ПК

РЕЖИМЫ 1D:
- Столбцы (гистограмма)
- Спираль по данным (r зависит от значения)
- Архимедова спираль (равномерная)
- Экспоненциальная спираль (золотой срез)

Разработчик: Судовский А.Л.
Москва, 2026"""

    text_widget = tk.Text(info_frame, wrap="word", bg="#F0F8FF", font=("Arial", 11))
    text_widget.insert("1.0", info_text)
    text_widget.config(state="disabled")
    text_widget.grid(row=0, column=0, sticky="nsew")

    contact_frame = Frame(about_window, bg="#E1ECF4", padx=10, pady=10)
    contact_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
    Label(
        contact_frame,
        text="Руководитель: Цвырко О.Л.",
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
    # Не блокируем другие окна - убираем grab_set() и wait_window()



def show_help():
    help_window = Toplevel()
    help_window.title("Справка")
    help_window.withdraw()
    if os.path.exists(ICON_PATH):
        try:
            help_window.iconbitmap(ICON_PATH)
        except:
            pass
    help_window.minsize(700, 500)

    help_window.grid_rowconfigure(0, weight=1)
    help_window.grid_columnconfigure(0, weight=1)
    help_window.configure(bg="#F0F8FF")

    tab_control = ttk.Notebook(help_window)
    tab_control.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Общая информация")
    tab_control.add(tab2, text="Математика")

    # Вкладка 1: Общая информация
    help_text1 = ("Хромоматематическое моделирование - программа для "
                  "исследования числовых закономерностей через цвет.\n\n"
                  "Основные возможности:\n"
                  "• Моделирование последовательности кубов (1D)\n"
                  "  - Четыре режима визуализации\n"
                  "  - Две цветовые модели\n\n"
                  "• Визуализация Ker-функции (2D)\n"
                  "  - Ker(x² + y²) и Ker(x³ + y³)\n"
                  "  - Цветовое кодирование\n\n"
                  "Управление:\n"
                  "• F1: Открыть справку\n"
                  "• Ctrl+F1: О программе\n\n"
                  "Опция 'Показывать значения' отображает числа на ячейках.")

    tab1.grid_rowconfigure(0, weight=1)
    tab1.grid_columnconfigure(0, weight=1)
    Label(
        tab1, text=help_text1, justify="left", font=("Arial", 10), wraplength=600
    ).grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Вкладка 2: Математика
    help_text2 = ("МАТЕМАТИЧЕСКИЕ ФОРМУЛЫ\n\n"
                  "1D РЕЖИМЫ:\n\n"
                  "Столбцы:\n"
                  "  height_i = (a_i / max_a) * (H - 50) * scale\n\n"
                  "Спираль по данным:\n"
                  "  theta_i = i * angle_step + rotation\n"
                  "  r_i = (a_i / max_a) * R_max\n\n"
                  "Архимедова спираль: r = a + b*theta\n"
                  "Экспоненциальная спираль: r = a * exp(b*theta)\n\n"
                  "2D РЕЖИМЫ:\n\n"
                  "Ker-функция (рекурсивная сумма цифр):\n"
                  "  Ker(n) = сумма цифр до однозначного числа\n"
                  "  Пример: Ker(38) = 3+8 = 11 → 1+1 = 2\n\n"
                  "Модели:\n"
                  "  Ker(x² + y²): сумма квадратов\n"
                  "  Ker(x³ + y³): сумма кубов")

    tab2.grid_rowconfigure(0, weight=1)
    tab2.grid_columnconfigure(0, weight=1)
    Label(
        tab2, text=help_text2, justify="left", font=("Arial", 10), wraplength=600
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
    # Не блокируем другие окна - убираем grab_set() и wait_window()

