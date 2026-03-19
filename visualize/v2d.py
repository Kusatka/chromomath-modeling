import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from visualize.hmm_module import model_ker_sum_squares, model_ker_sum_cubes


def resource_path(relative_path):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


ICON_PATH = os.path.join(resource_path(""), "icon.ico")


def center_window(win):
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
    win.title("Моделирование 2D")
    win.minsize(600, 400)
    if os.path.exists(ICON_PATH):
        win.iconbitmap(ICON_PATH)
    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(0, weight=1)
    main_frame = ttk.Frame(win)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    ctrl_frame = ttk.LabelFrame(main_frame, text="Управление моделью")
    ctrl_frame.grid(row=0, column=0, sticky="ns")
    canvas_frame = ttk.Frame(main_frame)
    canvas_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_columnconfigure(0, weight=1)
    info_frame = ttk.LabelFrame(main_frame, text="Информация")
    info_frame.grid(row=0, column=2, sticky="ns", padx=(10, 0))
    canvas = tk.Canvas(canvas_frame, bg="white", bd=1, relief="sunken")
    canvas.grid(row=0, column=0, sticky="nsew")
    export_btn = tk.Button(info_frame, text="Экспорт EPS", command=lambda: export_eps(), bg="#4A7B9D", fg="white", relief="flat")
    export_btn.pack(pady=(5, 0), fill="x")
    help_btn = tk.Button(info_frame, text="Справка", command=lambda: toggle_help(), bg="#E1ECF4", relief="flat")
    help_btn.pack(pady=(5, 0), fill="x")
    help_frame = tk.Frame(info_frame, bg="#F0F8FF", bd=1, relief="sunken")
    help_frame.pack(fill="both", expand=True, padx=5, pady=(5, 0))
    help_frame.pack_forget()
    help_text = tk.Text(help_frame, wrap="word", bg="#F0F8FF", font=("Arial", 10), padx=5, pady=5)
    help_text.insert("1.0", """Моделирование 2D
Возможные модели:
- Ker(x²+y²): Ker от суммы квадратов
- Ker(x³+y³): Ker от суммы кубов

Параметры:
- Цветовая модель:
    • Gradient по Ker — полный HSV-градиент по значению Ker
    • Mod N — дискретное представление по модулю N
- Диапазоны X и Y: поддерживают отрицательные значения для симметрии
- Размер ячейки влияет на масштаб рисунка
- Показывать значения - подписи внутри ячеек

Экспорт: Сохраняет сетку в EPS.

Ker(n) — рекурсивная сумма цифр до получения одного числа.
Пример: Ker(38) = 3+8 = 11 → 1+1 = 2""")
    help_text.config(state="disabled")
    help_text.pack(fill="both", expand=True)

    def toggle_help():
        if help_frame.winfo_ismapped():
            help_frame.pack_forget()
            help_btn.config(text="Справка")
        else:
            help_frame.pack(fill="both", expand=True, padx=5, pady=(5, 0))
            help_btn.config(text="Скрыть справку")

    models = {"Ker(x²+y²)": model_ker_sum_squares, "Ker(x³+y³)": model_ker_sum_cubes}
    palette_options = ["Gradient по Ker", "Mod N"]
    selected_palette = tk.StringVar(value=palette_options[0])
    model_var = tk.StringVar(value="Ker(x²+y²)")
    mod_n = tk.IntVar(value=7)
    show_values = tk.BooleanVar(value=True)
    cell_size = tk.IntVar(value=30)
    xmin_var = tk.StringVar(value="-15")
    xmax_var = tk.StringVar(value="15")
    ymin_var = tk.StringVar(value="-15")
    ymax_var = tk.StringVar(value="15")

    ttk.Label(ctrl_frame, text="Функция:").grid(row=0, column=0, sticky="w", pady=(5, 0))
    ttk.Combobox(ctrl_frame, textvariable=model_var, values=list(models.keys()), width=18, state="readonly").grid(row=0, column=1, sticky="w", pady=(5, 0))
    ttk.Label(ctrl_frame, text="Цветовая модель:").grid(row=1, column=0, sticky="w", pady=(5, 0))
    ttk.Combobox(ctrl_frame, textvariable=selected_palette, values=palette_options, width=18, state="readonly").grid(row=1, column=1, sticky="w", pady=(5, 0))
    mod_frame = ttk.Frame(ctrl_frame)
    ttk.Label(mod_frame, text="N:").pack(side="left")
    ttk.Entry(mod_frame, textvariable=mod_n, width=5).pack(side="left", padx=5)
    mod_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 10))
    ttk.Label(ctrl_frame, text="Диапазон X:").grid(row=3, column=0, sticky="w", pady=(0, 5))
    range_x = ttk.Frame(ctrl_frame)
    ttk.Entry(range_x, textvariable=xmin_var, width=5).pack(side="left")
    ttk.Label(range_x, text="до").pack(side="left", padx=2)
    ttk.Entry(range_x, textvariable=xmax_var, width=5).pack(side="left")
    range_x.grid(row=3, column=1, sticky="w", pady=(0, 5))
    ttk.Label(ctrl_frame, text="Диапазон Y:").grid(row=4, column=0, sticky="w", pady=(0, 5))
    range_y = ttk.Frame(ctrl_frame)
    ttk.Entry(range_y, textvariable=ymin_var, width=5).pack(side="left")
    ttk.Label(range_y, text="до").pack(side="left", padx=2)
    ttk.Entry(range_y, textvariable=ymax_var, width=5).pack(side="left")
    range_y.grid(row=4, column=1, sticky="w", pady=(0, 5))
    ttk.Label(ctrl_frame, text="Размер ячейки:").grid(row=5, column=0, sticky="w", pady=(0, 5))
    ttk.Scale(ctrl_frame, variable=cell_size, from_=10, to=80, orient="horizontal", length=150).grid(row=5, column=1, sticky="w", pady=(0, 10))
    ttk.Checkbutton(ctrl_frame, text="Показывать значения", variable=show_values).grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 10))
    ttk.Button(ctrl_frame, text="Построить модель", command=lambda: draw_model()).grid(row=7, column=0, columnspan=2, pady=(0, 10))

    def hsv_to_rgb(h, s=1.0, v=1.0):
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

    def get_color_2d(x, y, val):
        palette = selected_palette.get()
        if palette == "Gradient по Ker":
            ratio = val / 9
            hue = ratio * 360
            return hsv_to_rgb(hue)
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
            if xmin > xmax:
                xmin, xmax = xmax, xmin
            if ymin > ymax:
                ymin, ymax = ymax, ymin
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные диапазоны X/Y")
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
                    canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(val), font=("Arial", max(8, cell // 4)))
        for j, x in enumerate(range(xmin, xmax + 1)):
            canvas.create_text(j * cell + cell // 2, -15, text=str(x))
        for i, y in enumerate(range(ymin, ymax + 1)):
            canvas.create_text(-15, i * cell + cell // 2, text=str(y))
        canvas.config(scrollregion=(-20, -20, cols * cell + 20, rows * cell + 20))

    def export_eps():
        try:
            out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "2d_output.eps")
            canvas.postscript(file=out_path, colormode="color")
            messagebox.showinfo("Экспорт", f"Сетка сохранена в {out_path}")
        except Exception as e:
            messagebox.showerror("Ошибка экспорта", str(e))

    def update_mod_visibility_2d(*args):
        if selected_palette.get() == "Mod N":
            mod_frame.grid()
        else:
            mod_frame.grid_remove()

    selected_palette.trace_add("write", lambda *_: draw_model())
    selected_palette.trace_add("write", update_mod_visibility_2d)
    for var in [model_var, mod_n, show_values, cell_size, xmin_var, xmax_var, ymin_var, ymax_var]:
        var.trace_add("write", lambda *_: draw_model())

    def on_mousewheel(event):
        delta = 1 if event.delta > 0 else -1
        new_size = max(10, min(80, cell_size.get() + delta))
        cell_size.set(new_size)

    canvas.bind("<MouseWheel>", on_mousewheel)
    update_mod_visibility_2d()
    draw_model()
    win.update_idletasks()
    win.geometry("1000x700")
    center_window(win)
    win.mainloop()
