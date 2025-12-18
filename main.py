import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from data_generator import generate_cubes, save_cubes_to_file
from help_module import show_help, show_about
from visualize.v2d import v2d
from visualize.v1d import v1d

def resource_path(relative_path):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)

ICON_PATH = os.path.join(resource_path(""), "icon.ico")

def center_window(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"+{x}+{y}")
    root.deiconify()

def generate_data_dialog():
    dialog = tk.Toplevel()
    dialog.title("Генерация данных")
    dialog.minsize(300, 150)
    center_window(dialog)
    count_var = tk.StringVar(value="2000")
    ttk.Label(dialog, text="Количество кубов:").pack(pady=10)
    ttk.Entry(dialog, textvariable=count_var).pack(pady=5)
    def generate():
        try:
            count = int(count_var.get())
            cubes = generate_cubes(count)
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.txt")
            save_cubes_to_file(cubes, file_path)
            messagebox.showinfo("Успех", f"Сгенерировано {count} кубов")
            dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    ttk.Button(dialog, text="Генерировать", command=generate).pack(pady=10)

def main():
    root = tk.Tk()
    root.title("Хромоматематическое моделирование")
    root.minsize(400, 250)
    root.withdraw()
    if os.path.exists(ICON_PATH):
        root.iconbitmap(ICON_PATH)
    # Создание меню
    menu = tk.Menu(root)
    modeling_menu = tk.Menu(menu, tearoff=0)
    modeling_menu.add_command(label="1D", command=v1d)
    modeling_menu.add_command(label="2D", command=v2d)
    modeling_menu.add_separator()
    modeling_menu.add_command(label="Генерировать данные", command=generate_data_dialog)
    modeling_menu.add_command(label="Выход", command=root.destroy)
    help_menu = tk.Menu(menu, tearoff=0)
    help_menu.add_command(label="Справка", command=show_help)
    help_menu.add_command(label="О программе", command=show_about)
    menu.add_cascade(label="Моделирование", menu=modeling_menu)
    menu.add_cascade(label="Помощь", menu=help_menu)
    root.config(menu=menu)
    # Горячие клавиши
    root.bind_all("<F1>", lambda event: show_help())
    root.bind_all("<Control-F1>", lambda event: show_about())
    # Основной контейнер с адаптивной сеткой
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")
    # Настройка весов для растягивания
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    # Конфигурация строк/столбцов main_frame
    main_frame.grid_rowconfigure(0, weight=2)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_rowconfigure(2, weight=2)
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.grid_rowconfigure(4, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    # Элементы интерфейса
    tk.Label(main_frame, text="Хромоматематическое моделирование", font=("Arial", 14, "bold"), fg="#1E3F66").grid(row=0, column=0, pady=(20, 0), sticky="s")
    tk.Label(main_frame, text="Исследование числовых закономерностей", font=("Arial", 10)).grid(row=1, column=0, sticky="n")
    btn_frame = tk.Frame(main_frame)
    btn_frame.grid(row=2, column=0, sticky="nsew")
    btn_frame.grid_columnconfigure(0, weight=1)
    btn_frame.grid_columnconfigure(1, weight=1)
    tk.Button(btn_frame, text="1D", command=v1d, width=15, bg="#4A7B9D", fg="white").grid(row=0, column=0, padx=(20, 5), sticky="e")
    tk.Button(btn_frame, text="2D", command=v2d, width=15, bg="#3A6B8F", fg="white").grid(row=0, column=1, padx=(5, 20), sticky="w")
    tk.Label(main_frame, text="Нажмите F1 для справки", font=("Arial", 9), fg="#666666").grid(row=4, column=0, pady=(0, 15), sticky="n")
    # Центрирование
    center_window(root)
    root.mainloop()

if __name__ == "__main__":
    main()