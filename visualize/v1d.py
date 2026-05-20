import math
import os
import sys
import tkinter as tk
from tkinter import ttk


def resource_path(relative_path):
    """Получить абсолютный путь к файлу ресурса"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", relative_path)


ICON_PATH = resource_path("icon.ico")
DATA_PATH = resource_path("data/data.txt")

# Ограничение реально отрисовываемых элементов. Данные могут храниться в большем
# объёме, но Canvas получает только выбранное пользователем подмножество.
MIN_RENDER_POINTS = 30
DEFAULT_RENDER_POINTS = 150
MAX_RENDER_POINTS = 500


def load_data():
    """Загружает данные кубов из файла или генерирует их"""
    try:
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as file:
                data = [int(line.strip()) for line in file.readlines()]
                if data:
                    return data
    except Exception as e:
        print(f"[v1d] Ошибка загрузки данных: {e}")
    
    # Fallback: встроенная генерация данных
    print("[v1d] Использую встроенную генерацию данных (1³..3000³)")
    return [i**3 for i in range(1, 3001)]


# Загружаем данные один раз
data = load_data()


class TooltipLabel:
    """Простой тултип для отображения значения при наведении мыши"""
    def __init__(self, canvas):
        self.canvas = canvas
        self.tooltip_window = None
    
    def show(self, x, y, text):
        """Показать тултип на координатах x, y"""
        self.hide()
        
        self.tooltip_window = tw = tk.Toplevel(self.canvas)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=text, background="#FFFFCC", relief="solid", 
                         borderwidth=1, font=("Arial", 9))
        label.pack()
        
        # Автоматически скрыть через 3 секунды
        def auto_hide():
            if self.tooltip_window:
                try:
                    self.tooltip_window.destroy()
                except:
                    pass
                self.tooltip_window = None
        
        self.canvas.after(3000, auto_hide)
    
    def hide(self):
        """Скрыть тултип"""
        if self.tooltip_window:
            try:
                self.tooltip_window.destroy()
            except:
                pass
            self.tooltip_window = None


def hsv_to_rgb(h, s=1.0, v=1.0):
    """Конвертация HSV в RGB"""
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    r, g, b = {
        0: (c, x, 0),
        1: (x, c, 0),
        2: (0, c, x),
        3: (0, x, c),
        4: (x, 0, c),
        5: (c, 0, x),
    }[int(h / 60) % 6]
    return (
        f"#{int((r + m) * 255):02x}{int((g + m) * 255):02x}{int((b + m) * 255):02x}"
    )


def safe_int(value, default):
    """Безопасное преобразование пользовательского значения в int."""
    try:
        return int(value)
    except (TypeError, ValueError, tk.TclError):
        return default


def get_color(idx, value, palette, mod_n=2, rainbow_cycle=100):
    """Получить цвет для значения в зависимости от палитры"""
    if palette == "Радужный градиент":
        # Радужный цикл зависит от номера элемента (индекса), не от значения
        # Так каждый столбец/точка получит разный оттенок с чётким периодом
        cycle = max(safe_int(rainbow_cycle, 100), 2)
        ratio = (idx % cycle) / cycle
        hue = ratio * 360
        return hsv_to_rgb(hue)
    elif palette == "Mod N":
        n = max(safe_int(mod_n, 2), 2)
        intensity = int(255 * ((value % n) / (n - 1)))
        return f"#{intensity:02x}{intensity:02x}{intensity:02x}"
    return "#CCCCCC"


def v1d():
    """Окно 1D визуализации последовательности кубов"""
    win = tk.Toplevel()
    win.title("Хромоматематическое моделирование - 1D визуализация")
    win.withdraw()
    
    if os.path.exists(ICON_PATH):
        try:
            win.iconbitmap(ICON_PATH)
        except:
            pass
    
    win.minsize(600, 400)
    win.geometry("1400x850")
    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(0, weight=1)
    
    main_frame = tk.Frame(win)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    
    # === Левая панель управления ===
    ctrl_frame = tk.LabelFrame(main_frame, text="Параметры визуализации", padx=10, pady=10)
    ctrl_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))
    
    # === Правая область (граф + справка) ===
    right_frame = tk.Frame(main_frame)
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)
    
    # === Холст с прокруткой ===
    canvas_container = tk.Frame(right_frame)
    canvas_container.grid(row=0, column=0, sticky="nsew")
    canvas_container.grid_rowconfigure(0, weight=1)
    canvas_container.grid_columnconfigure(0, weight=1)
    
    canvas = tk.Canvas(canvas_container, bg="white")
    hbar = tk.Scrollbar(canvas_container, orient="horizontal", command=canvas.xview)
    vbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
    canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    
    vbar.grid(row=0, column=1, sticky="ns")
    hbar.grid(row=1, column=0, sticky="ew")
    canvas.grid(row=0, column=0, sticky="nsew")
    
    tooltip = TooltipLabel(canvas)
    
    # === Кнопка справки ===
    help_btn = tk.Button(right_frame, text="📘 Справка", command=lambda: toggle_help(),
                          bg="#E1ECF4", relief="flat")
    help_btn.grid(row=1, column=0, pady=(5, 0), sticky="ew")
    
    # === Фрейм справки ===
    help_frame = tk.Frame(right_frame, bg="#F0F8FF", bd=1, relief="sunken")
    help_text = tk.Text(help_frame, wrap="word", bg="#F0F8FF", font=("Arial", 9),
                        padx=10, pady=10, height=15)
    
    help_content = """╔═══════════════════════════════════════════════════════════╗
║  ХРОМОМАТЕМАТИЧЕСКОЕ МОДЕЛИРОВАНИЕ - РЕЖИМ 1D             ║
╚═══════════════════════════════════════════════════════════╝

ОСНОВНАЯ ИДЕЯ:
Последовательность n³ визуализируется выбранным числом точек.
Цвет показывает периодичность. Радиус/высота = математическое значение.

─────────────────────────────────────────────────────────────

📊 РЕЖИМ: СТОЛБЦЫ (гистограмма)
Формула:  height_i = (a_i / max(a)) × (H - 50) × масштаб
• Высота ∝ n³
• Ширина столбца регулируется
• Количество столбцов задаётся ползунком "Количество точек"
• Тултип: n и его куб

─────────────────────────────────────────────────────────────

🌀 РЕЖИМ: СПИРАЛЬ ПО ДАННЫМ
Полярные координаты:
  θ_i = i × шаг_угла + поворот
  r_i = (a_i / max(a)) × R_max
  x = x₀ + r·cos(θ),  y = y₀ + r·sin(θ)

• Угол = номер элемента (порядок)
• Радиус = математическое значение среди выбранных точек
• Пример: 100-й элемент (10^6) → дальше от центра
• Плотность: шаг угла между точками
• Радиус спирали: масштаб максимального радиуса

─────────────────────────────────────────────────────────────

🔄 РЕЖИМ: АРХИМЕДОВА СПИРАЛЬ  r = a + b×θ
Линейный рост радиуса с углом:
• Витки равномерно расположены
• Математическое значение → только цвет
• Количество витков: полные обороты (2π радиан)
• θ_i = (i / N) × 2π × витки + поворот
• r_i = a + b × θ_i  (радиус растёт линейно)

Хорошо видна периодичность цвета, ровная красивая спираль.

─────────────────────────────────────────────────────────────

📈 РЕЖИМ: ЭКСПОНЕНЦИАЛЬНАЯ СПИРАЛЬ  r = a × e^(b×θ)
Экспоненциальный рост (найдена в природе):
• Компромисс между двумя спиралями выше
• r_i = a × e^(b × θ_i)  (логарифмическая спираль)
• Коэффициент b (0.01-1.0): контролирует закрученность
  - 0.01: почти архимедова (слабая спираль)
  - 0.5: сбалансированная
  - 1.0: очень крутая (золотое сечение)
• Базовый радиус: начальное значение a

─────────────────────────────────────────────────────────────

🎨 ПАЛИТРЫ:
• Радужный градиент (HSV): периодический цвет
  Период цикла: после скольких элементов цвет повторяется
  
• Mod N: дискретные оттенки серого (0-255)
  N: модуль дискретизации (2-255)
  Цвет = 255 × ((a_i % N) / (N-1))

─────────────────────────────────────────────────────────────

⚙️ ОПТИМИЗАЦИЯ:
• Отрисовывается только выбранное число точек
• Перестроение выполняется по кнопке "Построить модель"
• Тултипы при наведении: n и его куб
• Масштаб: общий множитель для всех режимов

─────────────────────────────────────────────────────────────

💡 СОВЕТ:
Радужный градиент + низкий период = видна периодичность.
Mod N + большое N = видна структура в диапазонах.
Спираль по данным = честное представление роста кубов.
Архимедова спираль = эстетичная и ровная.
Экспоненциальная = "золотой срез" природы."""
    
    help_text.insert("1.0", help_content)
    help_text.config(state="disabled")
    help_text.pack(fill="both", expand=True)
    help_frame.grid_forget()
    
    def toggle_help():
        if help_frame.winfo_ismapped():
            help_frame.grid_forget()
            help_btn.config(text="📘 Справка")
        else:
            help_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
            help_btn.config(text="▲ Скрыть справку")
    
    # === Переменные ===
    vis_modes = ["Столбцы", "Спираль по данным", "Архимедова спираль", "Экспоненциальная спираль"]
    selected_vis = tk.StringVar(value="Спираль по данным")
    palette_options = ["Радужный градиент", "Mod N"]
    selected_palette = tk.StringVar(value="Радужный градиент")
    
    # Общие
    scale_factor = tk.DoubleVar(value=1.0)
    mod_n = tk.IntVar(value=7)
    rainbow_cycle = tk.IntVar(value=100)
    max_points_for_ui = min(MAX_RENDER_POINTS, len(data))
    initial_points = min(DEFAULT_RENDER_POINTS, max_points_for_ui)
    render_points = tk.DoubleVar(value=initial_points)
    
    # Столбцы
    bar_width = tk.DoubleVar(value=1.0)
    
    # Спираль по данным
    rotation_data = tk.DoubleVar(value=0.0)
    density_data = tk.DoubleVar(value=1.0)
    radius_data = tk.DoubleVar(value=1.0)
    
    # Архимедова спираль
    turns_archimedes = tk.DoubleVar(value=5.0)
    rotation_archimedes = tk.DoubleVar(value=0.0)
    
    # Экспоненциальная спираль
    coefficient_exp = tk.DoubleVar(value=0.15)
    base_radius_exp = tk.DoubleVar(value=10.0)
    rotation_exp = tk.DoubleVar(value=0.0)
    
    # === Построение UI ===
    row = 0
    
    # Выбор режима
    ttk.Label(ctrl_frame, text="Тип визуализации:", font=("Arial", 10, "bold")).grid(
        row=row, column=0, sticky="w", pady=(0, 5))
    row += 1
    
    mode_combo = ttk.Combobox(ctrl_frame, textvariable=selected_vis, values=vis_modes,
                               state="readonly", width=28)
    mode_combo.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    row += 1
    
    # Палитра
    ttk.Label(ctrl_frame, text="Цветовая модель:", font=("Arial", 10, "bold")).grid(
        row=row, column=0, sticky="w", pady=(0, 5))
    row += 1
    
    palette_combo = ttk.Combobox(ctrl_frame, textvariable=selected_palette,
                                  values=palette_options, state="readonly", width=28)
    palette_combo.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    row += 1
    
    # Параметры палитры - Mod N
    mod_frame = ttk.LabelFrame(ctrl_frame, text="Mod N")
    ttk.Label(mod_frame, text="N (модуль):").pack(side="left", padx=5)
    mod_spin = ttk.Spinbox(mod_frame, from_=2, to=255, textvariable=mod_n, width=5)
    mod_spin.pack(side="right", padx=(0, 5))
    mod_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    row += 1
    
    # Параметры палитры - Rainbow
    rainbow_frame = ttk.LabelFrame(ctrl_frame, text="Радужный градиент")
    ttk.Label(rainbow_frame, text="Период цикла:").pack(side="left", padx=5)
    rainbow_spin = ttk.Spinbox(rainbow_frame, from_=1, to=1000, textvariable=rainbow_cycle, width=5)
    rainbow_spin.pack(side="right", padx=(0, 5))
    rainbow_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    row += 1
    
    # Общий масштаб
    ttk.Label(ctrl_frame, text="Общий масштаб:").grid(row=row, column=0, sticky="w")
    scale_label = ttk.Label(ctrl_frame, text="1.00x")
    scale_label.grid(row=row, column=1, sticky="e")
    row += 1
    
    scale_slider = ttk.Scale(ctrl_frame, variable=scale_factor, from_=0.1, to=3.0,
                              orient="horizontal")
    scale_slider.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    row += 1

    # Количество элементов для отрисовки
    ttk.Label(ctrl_frame, text="Количество точек:").grid(row=row, column=0, sticky="w")
    points_label = ttk.Label(ctrl_frame, text=str(initial_points))
    points_label.grid(row=row, column=1, sticky="e")
    row += 1

    points_slider = ttk.Scale(
        ctrl_frame,
        variable=render_points,
        from_=min(MIN_RENDER_POINTS, max_points_for_ui),
        to=max_points_for_ui,
        orient="horizontal",
    )
    points_slider.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 15))
    row += 1
    
    # Фреймы для параметров каждого режима
    columns_frame = ttk.LabelFrame(ctrl_frame, text="Параметры: СТОЛБЦЫ")
    data_spiral_frame = ttk.LabelFrame(ctrl_frame, text="Параметры: СПИРАЛЬ ПО ДАННЫМ")
    archimedes_frame = ttk.LabelFrame(ctrl_frame, text="Параметры: АРХИМЕДОВА")
    exponential_frame = ttk.LabelFrame(ctrl_frame, text="Параметры: ЭКСПОНЕНЦИАЛЬНАЯ")
    
    # Столбцы параметры
    ttk.Label(columns_frame, text="Ширина столбца:").pack(anchor="w", padx=5, pady=(5, 0))
    bar_label = ttk.Label(columns_frame, text="1.00x")
    bar_label.pack(anchor="e", padx=5)
    bar_slider = ttk.Scale(columns_frame, variable=bar_width, from_=0.5, to=3.0,
                            orient="horizontal")
    bar_slider.pack(padx=5, pady=(0, 10), fill="x")
    
    # Спираль по данным параметры
    ttk.Label(data_spiral_frame, text="Угол поворота (град):").pack(anchor="w", padx=5, pady=(5, 0))
    rot_data_label = ttk.Label(data_spiral_frame, text="0°")
    rot_data_label.pack(anchor="e", padx=5)
    rot_data_slider = ttk.Scale(data_spiral_frame, variable=rotation_data, from_=0, to=360,
                                 orient="horizontal")
    rot_data_slider.pack(padx=5, pady=(0, 10), fill="x")
    
    ttk.Label(data_spiral_frame, text="Плотность точек:").pack(anchor="w", padx=5, pady=(5, 0))
    dens_label = ttk.Label(data_spiral_frame, text="1.00x")
    dens_label.pack(anchor="e", padx=5)
    dens_slider = ttk.Scale(data_spiral_frame, variable=density_data, from_=0.1, to=2.0,
                             orient="horizontal")
    dens_slider.pack(padx=5, pady=(0, 10), fill="x")
    
    ttk.Label(data_spiral_frame, text="Радиус спирали:").pack(anchor="w", padx=5, pady=(5, 0))
    rad_label = ttk.Label(data_spiral_frame, text="1.00x")
    rad_label.pack(anchor="e", padx=5)
    rad_slider = ttk.Scale(data_spiral_frame, variable=radius_data, from_=0.1, to=3.0,
                            orient="horizontal")
    rad_slider.pack(padx=5, pady=(0, 10), fill="x")
    
    # Архимедова спираль параметры
    ttk.Label(archimedes_frame, text="Количество витков:").pack(anchor="w", padx=5, pady=(5, 0))
    turns_label = ttk.Label(archimedes_frame, text="5.0")
    turns_label.pack(anchor="e", padx=5)
    turns_slider = ttk.Scale(archimedes_frame, variable=turns_archimedes, from_=1, to=20,
                              orient="horizontal")
    turns_slider.pack(padx=5, pady=(0, 10), fill="x")
    
    ttk.Label(archimedes_frame, text="Угол поворота (град):").pack(anchor="w", padx=5, pady=(5, 0))
    rot_arch_label = ttk.Label(archimedes_frame, text="0°")
    rot_arch_label.pack(anchor="e", padx=5)
    rot_arch_slider = ttk.Scale(archimedes_frame, variable=rotation_archimedes, from_=0, to=360,
                                 orient="horizontal")
    rot_arch_slider.pack(padx=5, pady=(0, 10), fill="x")
    
    # Экспоненциальная спираль параметры
    ttk.Label(exponential_frame, text="Коэффициент (0.01-1.0):").pack(anchor="w", padx=5, pady=(5, 0))
    coef_label = ttk.Label(exponential_frame, text="0.15")
    coef_label.pack(anchor="e", padx=5)
    coef_slider = ttk.Scale(exponential_frame, variable=coefficient_exp, from_=0.01, to=1.0,
                             orient="horizontal")
    coef_slider.pack(padx=5, pady=(0, 10), fill="x")
    
    ttk.Label(exponential_frame, text="Базовый радиус (пкс):").pack(anchor="w", padx=5, pady=(5, 0))
    base_rad_label = ttk.Label(exponential_frame, text="10.0")
    base_rad_label.pack(anchor="e", padx=5)
    base_rad_slider = ttk.Scale(exponential_frame, variable=base_radius_exp, from_=1, to=50,
                                 orient="horizontal")
    base_rad_slider.pack(padx=5, pady=(0, 10), fill="x")
    
    ttk.Label(exponential_frame, text="Угол поворота (град):").pack(anchor="w", padx=5, pady=(5, 0))
    rot_exp_label = ttk.Label(exponential_frame, text="0°")
    rot_exp_label.pack(anchor="e", padx=5)
    rot_exp_slider = ttk.Scale(exponential_frame, variable=rotation_exp, from_=0, to=360,
                                orient="horizontal")
    rot_exp_slider.pack(padx=5, pady=(0, 10), fill="x")
    
    # Добавляем фреймы в контрол-фрейм (изначально скрыты)
    columns_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    data_spiral_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    archimedes_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    exponential_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    row += 1

    build_btn = ttk.Button(
        ctrl_frame,
        text="Построить модель",
        command=lambda: build_model(),
    )
    build_btn.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(5, 5))
    row += 1

    status_label = ttk.Label(
        ctrl_frame,
        text="",
        foreground="#8A5A00",
        wraplength=230,
        justify="left",
    )
    status_label.grid(row=row, column=0, columnspan=2, sticky="ew")
    
    def show_only_params(*args):
        """Показать только параметры выбранного режима"""
        mode = selected_vis.get()
        columns_frame.grid_remove()
        data_spiral_frame.grid_remove()
        archimedes_frame.grid_remove()
        exponential_frame.grid_remove()
        
        if mode == "Столбцы":
            columns_frame.grid()
        elif mode == "Спираль по данным":
            data_spiral_frame.grid()
        elif mode == "Архимедова спираль":
            archimedes_frame.grid()
        elif mode == "Экспоненциальная спираль":
            exponential_frame.grid()
    
    def update_palette_visibility(*args):
        """Показать параметры выбранной палитры"""
        palette = selected_palette.get()
        if palette == "Mod N":
            mod_frame.grid()
            rainbow_frame.grid_remove()
        else:
            mod_frame.grid_remove()
            rainbow_frame.grid()
    
    def get_render_count():
        """Количество элементов, выбранное пользователем для текущей отрисовки."""
        upper_bound = max(1, min(MAX_RENDER_POINTS, len(data)))
        lower_bound = min(MIN_RENDER_POINTS, upper_bound)
        return max(lower_bound, min(int(round(render_points.get())), upper_bound))

    def mark_pending(*args):
        """Пометить модель как требующую перестроения."""
        status_label.config(text="Параметры изменены. Нажмите «Построить модель».")

    def build_model():
        """Перестроить модель по текущим параметрам."""
        status_label.config(text="")
        draw()

    def bind_tooltip(item_id, idx, val):
        """Привязать tooltip к объекту Canvas."""
        def on_enter(e, v=val, i_v=idx):
            tooltip.show(e.x_root, e.y_root, f"n = {i_v + 1}\nn³ = {v}")

        def on_leave(e):
            tooltip.hide()

        canvas.tag_bind(item_id, "<Enter>", on_enter)
        canvas.tag_bind(item_id, "<Leave>", on_leave)

    # === Функции отрисовки ===
    def draw_columns():
        if not data:
            return
        
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1 or h <= 1:
            return
        
        # Параметры отображения
        num_bars = get_render_count()
        bar_w = (w / num_bars) * bar_width.get()
        spacing = bar_w * 0.2
        total_w = num_bars * (bar_w + spacing)

        visible_indices = range(num_bars)
        visible_values = data[:num_bars]
        max_val = max(visible_values) if visible_values else 1
        
        canvas.config(scrollregion=(0, 0, total_w, h))
        
        for i, idx in enumerate(visible_indices):
            val = data[idx]
            # Высота от 0 до max_height_px, пропорционально значению
            max_height_px = (h - 50) * scale_factor.get()
            height = (val / max_val) * max_height_px if max_val > 0 else 0
            
            x0 = idx * (bar_w + spacing)
            y0 = h - height
            x1 = x0 + bar_w
            y1 = h
            
            color = get_color(idx, val, selected_palette.get(),
                            mod_n.get(), rainbow_cycle.get())
            rect_id = canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            
            bind_tooltip(rect_id, idx, val)
            
            if bar_w > 30:  # Показываем значение только если столбец достаточно широкий
                canvas.create_text(x0 + bar_w / 2, y0 - 15, text=str(val),
                                  font=("Arial", min(12, int(bar_w / 5))))
    
    def draw_spiral_data():
        """Спираль по данным: r ∝ значение, θ ∝ номер элемента"""
        if not data:
            return
        
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1 or h <= 1:
            return
        
        center_x, center_y = w / 2, h / 2
        num_points = get_render_count()
        visible_values = data[:num_points]
        max_val = max(visible_values)
        
        angle_step = 0.1 * density_data.get()
        scale = scale_factor.get() * radius_data.get()
        max_radius = min(w, h) / 2 * scale
        
        canvas.config(
            scrollregion=(
                center_x - max_radius - 20,
                center_y - max_radius - 20,
                center_x + max_radius + 20,
                center_y + max_radius + 20,
            )
        )
        
        # Собираем все координаты для полилинии
        line_coords = []
        point_data = []
        
        for i in range(num_points):
            angle = i * angle_step + math.radians(rotation_data.get())
            val = visible_values[i]
            radius = (val / max_val) * max_radius if max_val > 0 else 0
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            line_coords.extend([x, y])
            color = get_color(i, val, selected_palette.get(),
                            mod_n.get(), rainbow_cycle.get())
            size = max(1, int(1.5 * scale_factor.get()))
            point_data.append((x, y, color, size))
        
        # Рисуем полилинию (спираль)
        if len(line_coords) > 2:
            canvas.create_line(*line_coords, fill="#DDDDDD", width=1, smooth=False)
        
        # Рисуем точки сверху
        for idx, (x, y, color, size) in enumerate(point_data):
            point_id = canvas.create_oval(
                x - size, y - size, x + size, y + size, fill=color, outline=color
            )
            bind_tooltip(point_id, idx, visible_values[idx])



    
    def draw_spiral_archimedes():
        """Архимедова спираль: r = a + b*θ"""
        if not data:
            return
        
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1 or h <= 1:
            return
        
        center_x, center_y = w / 2, h / 2
        
        num_points = get_render_count()
        visible_values = data[:num_points]
        turns = turns_archimedes.get()
        theta_max = turns * 2 * math.pi
        
        max_radius = min(w, h) / 2 * scale_factor.get()
        b = max_radius / theta_max if theta_max > 0 else 1
        a = max_radius * 0.05
        
        canvas.config(
            scrollregion=(
                center_x - max_radius - 20,
                center_y - max_radius - 20,
                center_x + max_radius + 20,
                center_y + max_radius + 20,
            )
        )
        
        # Собираем координаты для полилинии
        line_coords = []
        point_data = []
        
        denom = max(num_points - 1, 1)
        rotation = math.radians(rotation_archimedes.get())
        for i in range(num_points):
            theta_base = (i / denom) * theta_max
            theta = theta_base + rotation
            radius = a + b * theta_base
            
            val = visible_values[i]
            x = center_x + radius * math.cos(theta)
            y = center_y + radius * math.sin(theta)
            
            line_coords.extend([x, y])
            color = get_color(i, val, selected_palette.get(),
                            mod_n.get(), rainbow_cycle.get())
            size = max(1, int(1.5 * scale_factor.get()))
            point_data.append((x, y, color, size))
        
        # Рисуем полилинию
        if len(line_coords) > 2:
            canvas.create_line(*line_coords, fill="#DDDDDD", width=1, smooth=False)
        
        # Рисуем точки сверху
        for idx, (x, y, color, size) in enumerate(point_data):
            point_id = canvas.create_oval(
                x - size, y - size, x + size, y + size, fill=color, outline=color
            )
            bind_tooltip(point_id, idx, visible_values[idx])


    
    def draw_spiral_exponential():
        """Экспоненциальная спираль: r = a * e^(b*θ)"""
        if not data:
            return
        
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <= 1 or h <= 1:
            return
        
        center_x, center_y = w / 2, h / 2
        
        num_points = get_render_count()
        visible_values = data[:num_points]
        b = coefficient_exp.get()
        a = base_radius_exp.get()
        
        # Ограничиваем рост экспоненты
        max_allowed_radius = min(w, h) / 2 * scale_factor.get()
        theta_max = math.log(max_allowed_radius / a + 0.001) / max(b, 0.001)
        
        canvas.config(
            scrollregion=(
                center_x - max_allowed_radius - 20,
                center_y - max_allowed_radius - 20,
                center_x + max_allowed_radius + 20,
                center_y + max_allowed_radius + 20,
            )
        )
        
        # Собираем координаты для полилинии
        line_coords = []
        point_data = []
        
        denom = max(num_points - 1, 1)
        rotation = math.radians(rotation_exp.get())
        for i in range(num_points):
            theta_base = (i / denom) * theta_max
            theta = theta_base + rotation
            
            try:
                radius = a * math.exp(b * theta_base)
                radius = min(radius, max_allowed_radius)
            except:
                radius = max_allowed_radius
            
            val = visible_values[i]
            x = center_x + radius * math.cos(theta)
            y = center_y + radius * math.sin(theta)
            
            line_coords.extend([x, y])
            color = get_color(i, val, selected_palette.get(),
                            mod_n.get(), rainbow_cycle.get())
            size = max(1, int(1.5 * scale_factor.get()))
            point_data.append((x, y, color, size))
        
        # Рисуем полилинию
        if len(line_coords) > 2:
            canvas.create_line(*line_coords, fill="#DDDDDD", width=1, smooth=False)
        
        # Рисуем точки сверху
        for idx, (x, y, color, size) in enumerate(point_data):
            point_id = canvas.create_oval(
                x - size, y - size, x + size, y + size, fill=color, outline=color
            )
            bind_tooltip(point_id, idx, visible_values[idx])


    
    def draw():
        """Главная функция отрисовки"""
        mode = selected_vis.get()
        
        if mode == "Столбцы":
            draw_columns()
        elif mode == "Спираль по данным":
            draw_spiral_data()
        elif mode == "Архимедова спираль":
            draw_spiral_archimedes()
        elif mode == "Экспоненциальная спираль":
            draw_spiral_exponential()
    
    # === Обновления UI ===
    def update_scale_label(*args):
        scale_label.config(text=f"{scale_factor.get():.2f}x")
        mark_pending()
    
    def update_bar_label(*args):
        bar_label.config(text=f"{bar_width.get():.2f}x")
        mark_pending()
    
    def update_rot_data_label(*args):
        rot_data_label.config(text=f"{rotation_data.get():.0f}°")
        mark_pending()
    
    def update_dens_label(*args):
        dens_label.config(text=f"{density_data.get():.2f}x")
        mark_pending()
    
    def update_rad_label(*args):
        rad_label.config(text=f"{radius_data.get():.2f}x")
        mark_pending()
    
    def update_turns_label(*args):
        turns_label.config(text=f"{turns_archimedes.get():.1f}")
        mark_pending()
    
    def update_rot_arch_label(*args):
        rot_arch_label.config(text=f"{rotation_archimedes.get():.0f}°")
        mark_pending()
    
    def update_coef_label(*args):
        coef_label.config(text=f"{coefficient_exp.get():.2f}")
        mark_pending()
    
    def update_base_rad_label(*args):
        base_rad_label.config(text=f"{base_radius_exp.get():.1f}")
        mark_pending()
    
    def update_rot_exp_label(*args):
        rot_exp_label.config(text=f"{rotation_exp.get():.0f}°")
        mark_pending()

    def update_points_label(*args):
        points_label.config(text=str(get_render_count()))
        mark_pending()
    
    # === Привязки ===
    def on_mode_change(*args):
        show_only_params()
        mark_pending()

    def on_palette_change(*args):
        update_palette_visibility()
        mark_pending()

    selected_vis.trace_add("write", on_mode_change)
    selected_palette.trace_add("write", on_palette_change)
    
    scale_factor.trace_add("write", update_scale_label)
    render_points.trace_add("write", update_points_label)
    bar_width.trace_add("write", update_bar_label)
    rotation_data.trace_add("write", update_rot_data_label)
    density_data.trace_add("write", update_dens_label)
    radius_data.trace_add("write", update_rad_label)
    turns_archimedes.trace_add("write", update_turns_label)
    rotation_archimedes.trace_add("write", update_rot_arch_label)
    coefficient_exp.trace_add("write", update_coef_label)
    base_radius_exp.trace_add("write", update_base_rad_label)
    rotation_exp.trace_add("write", update_rot_exp_label)
    mod_n.trace_add("write", lambda *a: mark_pending())
    rainbow_cycle.trace_add("write", lambda *a: mark_pending())
    
    # === События окна ===
    # Перерисовка намеренно выполняется только по кнопке "Построить модель":
    # это убирает лаги при изменении размера окна и движении слайдеров.
    win.bind("<MouseWheel>", lambda e: scale_factor.set(
        max(0.1, min(3.0, scale_factor.get() + (0.1 if e.delta > 0 else -0.1)))
    ))
    
    # === Центрирование окна ===
    def center_window():
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        win.geometry(f"+{x}+{y}")
    
    # === Инициализация ===
    show_only_params()
    update_palette_visibility()
    
    win.after(100, lambda: [build_model(), center_window()])
    win.deiconify()
