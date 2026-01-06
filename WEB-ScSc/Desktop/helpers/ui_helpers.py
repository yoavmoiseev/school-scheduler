import tkinter as tk
from tkinter import ttk
import school_scheduler.data.consts as consts

# style and lesson color caches
_style_cache = {}
lesson_color_map = {}

# Palette (bg, fg) pairs
palette = [
    ("yellow", "black"),
    ("gold", "black"),
    ("red", "white"),
    ("tomato", "white"),
    ("crimson", "white"),
    ("blue", "white"),
    ("dodgerblue", "white"),
    ("lightblue", "black"),
    ("green", "white"),
    ("limegreen", "black"),
    ("lightgreen", "black"),
    ("orange", "black"),
    ("darkorange", "white"),
    ("pink", "black"),
    ("hotpink", "white"),
    ("khaki", "black"),
    ("wheat", "black"),
    ("peachpuff", "black"),
    ("plum", "white"),
    ("violet", "white"),
    ("lightcoral", "black"),
    ("salmon", "black"),
    ("turquoise", "black"),
    ("mediumslateblue", "white")
]

def generate_color_pair(idx):
    return palette[idx % len(palette)]

def get_lesson_color(name):
    if name not in lesson_color_map:
        idx = len(lesson_color_map)
        lesson_color_map[name] = generate_color_pair(idx)
    return lesson_color_map[name]

def ensure_usable_theme(master):
    try:
        style = ttk.Style(master)
        current = style.theme_use()
        if current not in ("clam", "alt") and "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass

def set_cb_font(cb, fnt=("Arial", 24, "bold")):
    try:
        for child in cb.winfo_children():
            if isinstance(child, tk.Entry):
                child.configure(font=fnt)
                return
        try:
            entry = cb.nametowidget(cb.winfo_name() + ".entry")
            entry.configure(font=fnt)
        except Exception:
            pass
    except Exception:
        pass

def set_cb_color(cb, bg, fg="black", key=None, font_size=("Arial", 24, "bold")):
    try:
        master = cb.winfo_toplevel()
        ensure_usable_theme(master)
        style = ttk.Style(master)
        if key is None:
            key = f"{bg}|{fg}"
        style_name = _style_cache.get(key)
        if not style_name:
            safe_key = key.replace("|", "_").replace(" ", "_")
            style_name = f"CB_{safe_key}.TCombobox"
            style.configure(style_name,
                            fieldbackground=bg,
                            background=bg,
                            foreground=fg,
                            font=font_size)
            style.map(style_name,
                      fieldbackground=[('readonly', bg), ('disabled', bg), ('!disabled', bg)],
                      background=[('readonly', bg), ('disabled', bg), ('!disabled', bg)],
                      foreground=[('readonly', fg), ('disabled', fg), ('!disabled', fg)])
            _style_cache[key] = style_name
        cb.configure(style=style_name)
        cb.update_idletasks()
        set_cb_font(cb, fnt=font_size)
        return True
    except Exception:
        return False

def color_cb_by_content(cb):
    text = cb.get()
    if text == "":
        bg, fg = ("white", "black")
        key = "empty"
    elif text == consts.unavailable_slot:
        bg, fg = ("lightgray", "darkgray")
        key = "unavailable"
    else:
        bg, fg = get_lesson_color(text)
        key = f"lesson_{text}"
    set_cb_color(cb, bg, fg, key=key, font_size=("Arial", 24, "bold"))
