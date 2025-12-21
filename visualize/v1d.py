import math
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from .hmm_module import ker  # Относительный импорт, если нужен (хотя в v1d ker не используется напрямую)

def resource_path(relative_path):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)

ICON_PATH = os.path.join(resource_path(""), "icon.ico")

def load_data(count=2000):
    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data.txt")  # Подъём на уровень выше для data.txt в корне
        with open(file_path, "r") as file:
            data = [int(line.strip()) for line in file.readlines()]
        if len(data) < count:
            raise ValueError("Недостаточно данных в файле, сгенерируйте больше")
        return data[:count]
    except (FileNotFoundError, ValueError) as e:
        messagebox.showwarning("Предупреждение", f"Генерация данных на лету: {e}")
        return [i**3 for i in range(1, count + 1)]

def v1d():
    win = tk.Toplevel()
    win.title("Моделирование последовательности кубов")
    win.withdraw()
    if os.path.exists(ICON_PATH):
        win.iconbitmap(ICON_PATH)
    win.minsize(600, 400)
    win.geometry("1200x700")
    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(0, weight=1)
    main_frame = tk.Frame(win)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    # Левая панель управления
    ctrl_frame = tk.LabelFrame(main_frame, text="Параметры визуализации", padx=10, pady=10)
    ctrl_frame.grid(row=0, column=0, sticky="ns")
    # Правая область (график + справка)
    right_frame = tk.Frame(main_frame)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    # Холст с прокруткой
    canvas_container = tk.Frame(right_frame)
    canvas_container.pack(fill="both", expand=True)
    canvas_container.pack_propagate(False)
    canvas = tk.Canvas(canvas_container, bg="white")
    hbar = tk.Scrollbar(canvas_container, orient="horizontal", command=canvas.xview)
    vbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
    canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    vbar.pack(side="right", fill="y")
    hbar.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    # Кнопка справки
    help_btn = tk.Button(right_frame, text="📘 Справка", command=lambda: toggle_help(), bg="#E1ECF4", relief="flat")
    help_btn.pack(side="bottom", pady=(5, 0))
    # Кнопка экспорта
    export_btn = tk.Button(right_frame, text="Экспорт EPS", command=lambda: export_eps(), bg="#4A7B9D", fg="white", relief="flat")
    export_btn.pack(side="bottom", pady=(5, 0))

    help_frame = tk.Frame(right_frame, bg="#F0F8FF", bd=1, relief="sunken")
    help_text = tk.Text(help_frame, wrap="word", bg="#F0F8FF", font=("Arial", 10), padx=10, pady=10)
    help_text.insert("1.0", """Моделирование кубических последовательностей
Последовательность: n³ для n = 1,2,3,...
Параметры:
- Количество точек: задаёт длину последовательности
- Масштаб: регулирует размеры графика
- Тип визуализации:
  • Столбцы: классическая гистограмма
  • Спираль: траектория значений в полярных координатах
- Цветовая модель:
  • Радужный градиент: циклический цветовой переход (HSV)
  • Mod N: дискретное представление по модулю N

Параметр "Цикл радуги" означает, сколько точек нужно пройти, чтобы цветовой градиент повторился заново.
Экспорт: Сохраняет график в EPS для дальнейшего анализа.
""")
    help_text.config(state="disabled")
    help_text.pack(fill="both", expand=True)
    help_frame.pack_forget()

    def toggle_help():
        if help_frame.winfo_ismapped():
            help_frame.pack_forget()
            help_btn.config(text="📘 Справка")
        else:
            help_frame.pack(fill="x", pady=(5, 0))
            help_btn.config(text="▲ Скрыть справку")

    # Параметры визуализации
    vis_options = ["Столбцы", "Спираль"]
    selected_vis = tk.StringVar(value=vis_options[0])
    palette_options = ["Радужный градиент", "Mod N"]
    selected_palette = tk.StringVar(value=palette_options[0])
    mod_n = tk.StringVar(value="2")  # Теперь string для валидации
    rainbow_cycle = tk.StringVar(value="100")
    scale_factor = tk.DoubleVar(value=1.0)
    bar_width = tk.DoubleVar(value=1.0)
    rotation = tk.DoubleVar(value=0.0)
    spiral_density = tk.DoubleVar(value=1.0)
    spiral_radius_factor = tk.DoubleVar(value=1.0)
    count_var = tk.StringVar(value="100")  # Базовое 100
    # Фреймы для настроек столбцов и спирали
    cols_params_frame = ttk.LabelFrame(ctrl_frame, text="Параметры столбцов")
    spiral_params_frame = ttk.LabelFrame(ctrl_frame, text="Параметры спирали")
    # Элементы управления
    ttk.Label(ctrl_frame, text="Количество точек:").grid(row=0, column=0, sticky="w", pady=(0, 5))
    count_entry = ttk.Entry(ctrl_frame, textvariable=count_var, width=10, validate="key")
    count_entry['validatecommand'] = (ctrl_frame.register(lambda s: s.isdigit()), "%P")  # Только цифры
    count_entry.grid(row=0, column=1, sticky="w", pady=(0, 5))
    ttk.Label(ctrl_frame, text="Тип визуализации:").grid(row=1, column=0, sticky="w", pady=(0, 5))
    ttk.Combobox(ctrl_frame, textvariable=selected_vis, values=vis_options, state="readonly", width=18).grid(row=1, column=1, sticky="w", pady=(0, 5))
    ttk.Label(ctrl_frame, text="Цветовая модель:").grid(row=2, column=0, sticky="w", pady=(0, 5))
    ttk.Combobox(ctrl_frame, textvariable=selected_palette, values=palette_options, state="readonly", width=18).grid(row=2, column=1, sticky="w", pady=(0, 5))
    # Mod N
    mod_frame = ttk.Frame(ctrl_frame)
    ttk.Label(mod_frame, text="N для Mod N:").pack(side="left")
    mod_entry = ttk.Entry(mod_frame, textvariable=mod_n, width=5, validate="key")
    mod_entry['validatecommand'] = (ctrl_frame.register(lambda s: s.isdigit()), "%P")  # Только цифры
    mod_entry.pack(side="right", padx=(5, 0))
    mod_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 10))
    # Цикл радуги
    rainbow_frame = ttk.Frame(ctrl_frame)
    ttk.Label(rainbow_frame, text="Цикл радуги:").pack(side="left")
    rainbow_entry = ttk.Entry(rainbow_frame, textvariable=rainbow_cycle, width=5, validate="key")
    rainbow_entry['validatecommand'] = (ctrl_frame.register(lambda s: s.isdigit()), "%P")  # Только цифры
    rainbow_entry.pack(side="right", padx=(5, 0))
    rainbow_frame.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 10))
    # Масштаб
    ttk.Label(ctrl_frame, text="Масштаб:").grid(row=5, column=0, sticky="w", pady=(0, 5))
    ttk.Scale(ctrl_frame, variable=scale_factor, from_=0.1, to=3.0, orient="horizontal", length=160).grid(row=5, column=1, sticky="w", pady=(0, 10))
    # Параметры столбцов
    cols_params_frame.grid(row=6, column=0, columnspan=2, sticky="we", pady=(0, 10))
    ttk.Label(cols_params_frame, text="Ширина столбца:").pack(anchor="w", padx=5, pady=(5, 0))
    ttk.Scale(cols_params_frame, variable=bar_width, from_=0.5, to=3.0, orient="horizontal", length=140).pack(padx=5, pady=(0, 10))
    # Параметры спирали
    spiral_params_frame.grid(row=7, column=0, columnspan=2, sticky="we")
    ttk.Label(spiral_params_frame, text="Угол поворота:").pack(anchor="w", padx=5, pady=(5, 0))
    ttk.Scale(spiral_params_frame, variable=rotation, from_=0, to=360, orient="horizontal", length=150).pack(padx=5, pady=(0, 5))
    ttk.Label(spiral_params_frame, text="Плотность точек:").pack(anchor="w", padx=5, pady=(5, 0))
    ttk.Scale(spiral_params_frame, variable=spiral_density, from_=0.1, to=2.0, orient="horizontal", length=150).pack(padx=5, pady=(0, 5))
    ttk.Label(spiral_params_frame, text="Радиус спирали:").pack(anchor="w", padx=5, pady=(5, 0))
    ttk.Scale(spiral_params_frame, variable=spiral_radius_factor, from_=0.1, to=3.0, orient="horizontal", length=150).pack(padx=5, pady=(0, 10))

    def hsv_to_rgb(h, s=1.0, v=1.0):
        """Конвертация HSV в RGB (улучшено для полного спектра)"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        return f"#{int((r + m) * 255):02x}{int((g + m) * 255):02x}{int((b + m) * 255):02x}"

    def get_color(idx, value):
        palette = selected_palette.get()
        try:
            if palette == "Радужный градиент":
                cycle = max(int(rainbow_cycle.get() or 100), 2)  # Fallback если пусто
                ratio = (value % cycle) / cycle
                hue = ratio * 360
                return hsv_to_rgb(hue)
            elif palette == "Mod N":
                n = max(int(mod_n.get() or 2), 2)  # Fallback если пусто
                intensity = int(255 * ((value % n) / (n - 1)))
                return f"#{intensity:02x}{intensity:02x}{intensity:02x}"
        except ValueError:
            return "#CCCCCC"  # Тихий fallback, без messagebox здесь

    def draw_columns(data):
        if not data:
            return
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1 or h <= 1:
            return
        max_val = max(data)
        num_bars = len(data)
        total_spacing = num_bars + 1
        bar_w = max(1, (w - total_spacing) / num_bars * bar_width.get())  # Улучшенный расчёт для предотвращения слияния
        spacing = 1  # Минимальный spacing
        total_w = num_bars * bar_w + total_spacing
        max_height_px = (h - 50) * scale_factor.get()
        y0_min = h - max_height_px
        canvas.config(scrollregion=(0, y0_min, total_w, h))

        for i, val in enumerate(data):
            height = (val / max_val) * (h - 50) * scale_factor.get()
            x0 = i * (bar_w + spacing) + spacing
            y0 = h - height
            x1 = x0 + bar_w
            y1 = h
            color = get_color(i, val)
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            if bar_w > 20:
                canvas.create_text(x0 + bar_w / 2, y0 - 15, text=str(val), font=("Arial", min(12, int(bar_w / 5))))

    def draw_spiral(data):
        if not data:
            return
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1 or h <= 1:
            return
        center_x, center_y = w / 2, h / 2
        max_val = max(data)
        angle_step = 0.1 * spiral_density.get()
        scale = scale_factor.get() * spiral_radius_factor.get()
        num_points = len(data)
        max_radius = min(w, h) / 2 * scale
        points = []
        for i in range(num_points):
            angle = i * angle_step + math.radians(rotation.get())
            val = data[i]
            radius = (val / max_val) * max_radius
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
            if center_x - max_radius <= x <= center_x + max_radius and center_y - max_radius <= y <= center_y + max_radius:
                color = get_color(i, val)
                size = max(1, int(1 * scale_factor.get()))
                canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline=color)
        if points:
            for i in range(1, len(points)):
                if abs(points[i][0] - points[i - 1][0]) < w and abs(points[i][1] - points[i - 1][1]) < h:
                    canvas.create_line(points[i - 1][0], points[i - 1][1], points[i][0], points[i][1], fill="#AAAAAA", smooth=True, width=1)
        canvas.config(scrollregion=(0, 0, w, h))

    def draw():
        try:
            count = max(1, int(count_var.get() or 100))  # Fallback если пусто
            data = load_data(count)
            if selected_vis.get() == "Столбцы":
                draw_columns(data)
            else:
                draw_spiral(data)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def export_eps():
        try:
            canvas.postscript(file="1d_output.eps", colormode='color')
            messagebox.showinfo("Экспорт", "График сохранён в 1d_output.eps")
        except Exception as e:
            messagebox.showerror("Ошибка экспорта", str(e))

    def toggle_params(*args):
        if selected_vis.get() == "Столбцы":
            cols_params_frame.grid()
            spiral_params_frame.grid_remove()
        else:
            cols_params_frame.grid_remove()
            spiral_params_frame.grid()

    def update_mod_visibility_1d(*args):
        if selected_palette.get() == "Mod N":
            mod_frame.grid()
        else:
            mod_frame.grid_remove()

    def update_rainbow_visibility(*args):
        if selected_palette.get() == "Радужный градиент":
            rainbow_frame.grid()
        else:
            rainbow_frame.grid_remove()

    selected_vis.trace_add("write", toggle_params)
    selected_palette.trace_add("write", lambda *_: draw())
    selected_palette.trace_add("write", update_mod_visibility_1d)
    selected_palette.trace_add("write", update_rainbow_visibility)
    update_mod_visibility_1d()
    update_rainbow_visibility()
    toggle_params()
    for var in [selected_vis, selected_palette, mod_n, rainbow_cycle, scale_factor, bar_width, rotation, spiral_density, spiral_radius_factor, count_var]:
        var.trace_add("write", lambda *_: win.after(200, draw))  # Delay 200ms для ввода без мгновенной ошибки

    win.bind("<Configure>", lambda e: win.after(100, draw))
    win.bind("<MouseWheel>", lambda e: scale_factor.set(max(0.1, min(3.0, scale_factor.get() + (0.1 if e.delta > 0 else -0.1)))))

    # Центрирование
    def center_window():
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        win.geometry(f"+{x}+{y}")

    # Отрисовка с центрированием
    def draw_wrapper():
        draw()
        center_window()
        win.after(100, center_window)

    win.after(100, draw_wrapper)
    win.deiconify()