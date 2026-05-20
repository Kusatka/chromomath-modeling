import os
import sys
import tkinter as tk
from tkinter import ttk
from visualize.hmm_module import model_ker_sum_squares, model_ker_sum_cubes


def resource_path(relative_path):
    """Получить абсолютный путь к файлу ресурса"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", relative_path)


ICON_PATH = resource_path("icon.ico")


def center_window(win):
    """Центрирует окно на экране"""
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"+{x}+{y}")


def v2d():
    win = tk.Toplevel()
    win.title("Хромоматематическое моделирование - 2D визуализация")
    win.withdraw()
    
    if os.path.exists(ICON_PATH):
        try:
            win.iconbitmap(ICON_PATH)
        except:
            pass
    
    win.minsize(600, 400)
    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(0, weight=1)
    main_frame = ttk.Frame(win)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    # Левая панель управления
    ctrl_frame = ttk.LabelFrame(main_frame, text="Управление моделью")
    ctrl_frame.grid(row=0, column=0, sticky="ns")
    # Центральная область - холст
    canvas_frame = ttk.Frame(main_frame)
    canvas_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_columnconfigure(0, weight=1)
    # Правая панель - информация + справка
    info_frame = ttk.LabelFrame(main_frame, text="Информация")
    info_frame.grid(row=0, column=2, sticky="ns", padx=(10, 0))
    # Холст
    canvas = tk.Canvas(canvas_frame, bg="white", bd=1, relief="sunken")
    canvas.grid(row=0, column=0, sticky="nsew")
    # Кнопка справки и её фрейм внутри info_frame
    help_btn = tk.Button(
        info_frame,
        text="📘 Справка",
        command=lambda: toggle_help(),
        bg="#E1ECF4",
        relief="flat",
    )
    help_btn.pack(pady=(5, 0), fill="x")
    help_frame = tk.Frame(info_frame, bg="#F0F8FF", bd=1, relief="sunken")
    help_frame.pack(fill="both", expand=True, padx=5, pady=(5, 0))
    help_frame.pack_forget()

    help_text = tk.Text(
        help_frame, wrap="word", bg="#F0F8FF", font=("Arial", 10), padx=5, pady=5
    )
    help_text.insert(
        "1.0",
        """Моделирование 2D
Возможные модели:
- Ker(x²+y²): Ker от суммы квадратов
- Ker(x³+y³): Ker от суммы кубов

Параметры:
- Цветовая модель:
    • Gradient по Ker — градиент по значению Ker
    • Mod N — дискретное представление по модулю N
- Диапазоны X и Y задают размер сетки
- Размер ячейки влияет на масштаб рисунка
- Показывать значения - подписи внутри ячеек

Ker(n) — рекурсивная сумма цифр до получения одного числа.
Пример: Ker(38) = 3+8 = 11 → 1+1 = 2
""",
    )
    help_text.config(state="disabled")
    help_text.pack(fill="both", expand=True)

    def toggle_help():
        if help_frame.winfo_ismapped():
            help_frame.pack_forget()
            help_btn.config(text="📘 Справка")
        else:
            help_frame.pack(fill="both", expand=True, padx=5, pady=(5, 0))
            help_btn.config(text="▲ Скрыть справку")

    # Параметры моделей
    models = {"Ker(x²+y²)": model_ker_sum_squares, "Ker(x³+y³)": model_ker_sum_cubes}
    palette_options = ["Gradient по Ker", "Mod N"]
    selected_palette = tk.StringVar(value=palette_options[0])
    model_var = tk.StringVar(value="Ker(x²+y²)")
    mod_n = tk.IntVar(value=7)
    show_values = tk.BooleanVar(value=True)
    cell_size = tk.IntVar(value=30)
    xmin_var = tk.StringVar(value="1")
    xmax_var = tk.StringVar(value="15")
    ymin_var = tk.StringVar(value="1")
    ymax_var = tk.StringVar(value="15")
    # Элементы управления
    ttk.Label(ctrl_frame, text="Функция:").grid(
        row=0, column=0, sticky="w", pady=(5, 0)
    )
    ttk.Combobox(
        ctrl_frame,
        textvariable=model_var,
        values=list(models.keys()),
        width=18,
        state="readonly",
    ).grid(row=0, column=1, sticky="w", pady=(5, 0))
    ttk.Label(ctrl_frame, text="Цветовая модель:").grid(
        row=1, column=0, sticky="w", pady=(5, 0)
    )
    ttk.Combobox(
        ctrl_frame,
        textvariable=selected_palette,
        values=palette_options,
        width=18,
        state="readonly",
    ).grid(row=1, column=1, sticky="w", pady=(5, 0))
    mod_frame = ttk.Frame(ctrl_frame)
    ttk.Label(mod_frame, text="N:").pack(side="left")
    ttk.Entry(mod_frame, textvariable=mod_n, width=5).pack(side="left", padx=5)
    mod_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 10))
    ttk.Label(ctrl_frame, text="Диапазон X:").grid(
        row=3, column=0, sticky="w", pady=(0, 5)
    )
    range_x = ttk.Frame(ctrl_frame)
    ttk.Entry(range_x, textvariable=xmin_var, width=5).pack(side="left")
    ttk.Label(range_x, text="до").pack(side="left", padx=2)
    ttk.Entry(range_x, textvariable=xmax_var, width=5).pack(side="left")
    range_x.grid(row=3, column=1, sticky="w", pady=(0, 5))
    ttk.Label(ctrl_frame, text="Диапазон Y:").grid(
        row=4, column=0, sticky="w", pady=(0, 5)
    )
    range_y = ttk.Frame(ctrl_frame)
    ttk.Entry(range_y, textvariable=ymin_var, width=5).pack(side="left")
    ttk.Label(range_y, text="до").pack(side="left", padx=2)
    ttk.Entry(range_y, textvariable=ymax_var, width=5).pack(side="left")
    range_y.grid(row=4, column=1, sticky="w", pady=(0, 5))
    ttk.Label(ctrl_frame, text="Размер ячейки:").grid(
        row=5, column=0, sticky="w", pady=(0, 5)
    )
    size_frame = ttk.Frame(ctrl_frame)
    size_frame.grid(row=5, column=1, sticky="w", pady=(0, 10))
    ttk.Scale(
        size_frame, variable=cell_size, from_=10, to=80, orient="horizontal", length=120
    ).pack(side="left")
    cell_size_label = ttk.Label(size_frame, text="10 px", width=6)
    cell_size_label.pack(side="left", padx=(5, 0))
    
    def update_cell_size_label(var, index, mode):
        cell_size_label.config(text=f"{int(cell_size.get())} px")
    
    cell_size.trace_add("write", update_cell_size_label)

    ttk.Checkbutton(ctrl_frame, text="Показывать значения", variable=show_values).grid(
        row=6, column=0, columnspan=2, sticky="w", pady=(0, 10)
    )
    ttk.Button(ctrl_frame, text="Построить модель", command=lambda: draw_model()).grid(
        row=7, column=0, columnspan=2, pady=(0, 10)
    )

    def get_color_2d(x, y, val):
        palette = selected_palette.get()
        if palette == "Gradient по Ker":
            ratio = (val % 10) / 10
            r = int(255 * (1 - ratio))
            g = int(255 * ratio)
            return f"#{r:02x}{g:02x}80"
        elif palette == "Mod N":
            try:
                n_val = mod_n.get()
                n = max(n_val, 2)
            except (tk.TclError, ValueError):
                n = 2
            intensity = int(255 * ((val % n) / (n - 1)))
            return f"#{intensity:02x}{intensity:02x}{intensity:02x}"
        return "#CCCCCC"

    def draw_model():
        canvas.delete("all")
        try:
            xmin = int(xmin_var.get())
            xmax = int(xmax_var.get())
            ymin = int(ymin_var.get())
            ymax = int(ymax_var.get())
        except ValueError:
            return
        cell = cell_size.get()
        model_func = models[model_var.get()]
        rows = ymax - ymin + 1
        cols = xmax - xmin + 1
        for i, y in enumerate(range(ymin, ymax + 1)):
            for j, x in enumerate(range(xmin, xmax + 1)):
                val = model_func(x, y)
                color = get_color_2d(x, y, val)
                x0 = j * cell
                y0 = i * cell
                x1 = x0 + cell
                y1 = y0 + cell
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
                if show_values.get():
                    canvas.create_text(
                        (x0 + x1) // 2,
                        (y0 + y1) // 2,
                        text=str(val),
                        font=("Arial", max(8, cell // 4)),
                    )
        # Подписи осей
        for j, x in enumerate(range(xmin, xmax + 1)):
            canvas.create_text(j * cell + cell // 2, -15, text=str(x))
        for i, y in enumerate(range(ymin, ymax + 1)):
            canvas.create_text(-15, i * cell + cell // 2, text=str(y))
        canvas.config(scrollregion=(-20, -20, cols * cell + 20, rows * cell + 20))

    def update_mod_visibility_2d(*args):
        if selected_palette.get() == "Mod N":
            mod_frame.grid()
        else:
            mod_frame.grid_remove()

    selected_palette.trace_add("write", lambda *_: draw_model())
    selected_palette.trace_add("write", update_mod_visibility_2d)
    for var in [model_var, mod_n, show_values, cell_size]:
        var.trace_add("write", lambda *_: draw_model())

    def on_mousewheel(event):
        delta = 1 if event.delta > 0 else -1
        new_size = max(10, min(80, cell_size.get() + delta))
        cell_size.set(new_size)

    canvas.bind("<MouseWheel>", on_mousewheel)
    
    # Инициализация
    update_mod_visibility_2d()
    draw_model()
    
    # Центрирование и отображение окна
    win.update_idletasks()
    win.geometry("1000x700")
    center_window(win)
    win.deiconify()
