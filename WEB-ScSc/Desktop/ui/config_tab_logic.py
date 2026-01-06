# config_tab_logic.py
import os
import shutil
from tkinter import messagebox
from school_scheduler.ui.translations import GUI_TEXT
from ui.global_config import (
    _gather_current_config, _apply_to_consts,
    reload_consts, save_consts_to_disk,
    SOURCE_FILE, TARGET_FILE
)

# ---------------------------
# TREE / SLOTS LOGIC
# ---------------------------
def populate_tree(tree, lessons_var, current_cfg):
    """
    Заполнить tree текущими значениями TIME_SLOTS из current_cfg.
    Принимает сам виджет tree, lessons_var (IntVar) и текущую конфигурацию (dict).
    """
    tree.delete(*tree.get_children())
    ts = current_cfg.get("TIME_SLOTS", {})
    try:
        lessons_count = int(lessons_var.get())
    except Exception:
        lessons_count = len(current_cfg.get("LESSONS", []))
    for i in range(1, lessons_count + 1):
        tree.insert("", "end", iid=str(i), values=(i, ts.get(i, "")))

def add_or_update_slot(tree, edit_lesson_var, edit_time_var):
    """
    Добавляет или обновляет слот в tree (по номеру урока).
    """
    try:
        ln = int(edit_lesson_var.get())
    except Exception:
        # если не число — ничего не делаем
        return
    t = edit_time_var.get().strip()
    iid = str(ln)

    # если узел существует — удалить его (чтобы вставить на нужную позицию)
    if iid in tree.get_children():
        tree.delete(iid)

    # найти позицию вставки по порядку
    children = tree.get_children()
    pos = "end"
    for i, child in enumerate(children):
        try:
            child_int = int(child)
            if ln < child_int:
                pos = i
                break
        except Exception:
            continue

    tree.insert("", pos, iid=iid, values=(ln, t))

def delete_slot(tree, edit_lesson_var):
    """
    Удаляет слот по номеру урока (если существует).
    """
    ln = str(edit_lesson_var.get())
    if ln in tree.get_children():
        tree.delete(ln)

# ---------------------------
# SAVE / RELOAD / RESET LOGIC
# ---------------------------
def on_save_logic(app, current_cfg, vars_dict, tree, weekdays_txt):
    """
    Сохранение конфигурации — логика вынесена сюда.
        vars_dict должен содержать:
            "gui_lang_var","app_name_var","app_size_var","afd_var","retries_var","lessons_var",
            "max_sequence_lessons_var","max_per_day_var"
    """
    # Ask for confirmation before saving
    if not messagebox.askyesno(GUI_TEXT[153], GUI_TEXT[199], default=messagebox.NO):  # "Confirm", "Are you sure you want to save..."
        return
    
    cfg = _gather_current_config()

    # основные поля из UI
    cfg["GUI_LANGUAGE"] = vars_dict["gui_lang_var"].get()
    cfg["app_name"] = vars_dict["app_name_var"].get()
    cfg["app_size"] = vars_dict["app_size_var"].get()
    cfg["autofill_direction"] = vars_dict["afd_var"].get()
    try:
        cfg["max_autofill_retries"] = int(vars_dict["retries_var"].get())
    except Exception:
        cfg["max_autofill_retries"] = current_cfg.get("max_autofill_retries", 0)

    # new scheduling limits
    try:
        cfg["max_sequence_lessons"] = int(vars_dict.get("max_sequence_lessons_var").get())
    except Exception:
        cfg["max_sequence_lessons"] = current_cfg.get("max_sequence_lessons", 2)

    try:
        cfg["max_per_day"] = int(vars_dict.get("max_per_day_var").get())
    except Exception:
        cfg["max_per_day"] = current_cfg.get("max_per_day", 3)

    # LESSONS
    try:
        lessons_count = int(vars_dict["lessons_var"].get())
    except Exception:
        lessons_count = len(current_cfg.get("LESSONS", []))
    cfg["LESSONS"] = list(range(1, lessons_count + 1))

    # TIME_SLOTS: собрать из tree
    ts = {}
    for iid in tree.get_children():
        vals = tree.item(iid, "values")
        try:
            k = int(vals[0])
            ts[k] = vals[1]
        except Exception:
            pass
    cfg["TIME_SLOTS"] = ts

    # Weekdays из текстового поля
    sel_lang = vars_dict["gui_lang_var"].get()
    text_days = [line.strip() for line in weekdays_txt.get("1.0", "end").splitlines() if line.strip()]
    if sel_lang not in cfg.get("TEXTS", {}):
        cfg.setdefault("TEXTS", {})[sel_lang] = {}
    cfg["TEXTS"][sel_lang]["weekdays"] = text_days
    cfg["WEEKDAYS"] = text_days

    # Hidden preserve
    cfg["HIDDEN"] = current_cfg.get("HIDDEN", {})

    # Применить и сохранить
    _apply_to_consts(cfg)
    ok = save_consts_to_disk(cfg)
    if ok:
        try:
            app.root.title(cfg["app_name"])
        except Exception:
            pass
        messagebox.showinfo(GUI_TEXT[187], GUI_TEXT[188])  # "Config", "The configuration successfully saved."
    else:
        messagebox.showerror(GUI_TEXT[187], GUI_TEXT[189])  # "Config", "Failed to save consts.py (see console)."

def on_reload_logic(app, current_cfg, vars_dict, populate_tree_func, load_weekdays_func=None):
    """
    Полный перезапуск приложения для перезагрузки всей конфигурации и UI.
    """
    import sys
    import subprocess
    import tkinter as tk
    from . import translations as tr
    
    # Ask for confirmation before reloading (default NO)
    if not messagebox.askyesno(
        tr.GUI_TEXT[153],  # "Confirm"
        tr.GUI_TEXT[125],  # "Are you sure you want to reload..."
        default=messagebox.NO
    ):
        return
    
    # Close current window
    root = tk._get_default_root()
    if root:
        root.quit()
        root.destroy()
    
    # Start new process
    env = os.environ.copy()
    if getattr(sys, 'frozen', False):
        # Running as EXE: sys.executable is the EXE path
        subprocess.Popen([sys.executable] + sys.argv[1:], env=env)
    else:
        # Running as script: need python + script path
        subprocess.Popen([sys.executable] + sys.argv, env=env)
    sys.exit()

    try:
        vars_dict["app_name_var"].set(current["app_name"])
    except Exception:
        pass
    try:
        vars_dict["app_size_var"].set(current["app_size"])
    except Exception:
        pass
    try:
        vars_dict["gui_lang_var"].set(current["GUI_LANGUAGE"])
    except Exception:
        pass
    try:
        vars_dict["afd_var"].set(current["autofill_direction"])
    except Exception:
        pass
    try:
        vars_dict["retries_var"].set(current["max_autofill_retries"])
    except Exception:
        pass
    try:
        vars_dict["lessons_var"].set(len(current.get("LESSONS", [])))
    except Exception:
        pass
    try:
        vars_dict.get("max_sequence_lessons_var").set(current.get("max_sequence_lessons", 2))
    except Exception:
        pass
    try:
        vars_dict.get("max_per_day_var").set(current.get("max_per_day", 3))
    except Exception:
        pass

    # Обновляем ссылку-на-словарь current_cfg, чтобы внешняя ссылка увидела изменения
    try:
        current_cfg.clear()
        current_cfg.update(current)
    except Exception:
        pass

    # восстановить tree и weekdays
    try:
        populate_tree_func()
    except Exception:
        pass
    if load_weekdays_func:
        try:
            load_weekdays_func()
        except Exception:
            pass

    messagebox.showinfo(GUI_TEXT[187], GUI_TEXT[190])  # "Config", "Reloaded from consts.py"

def on_reset_defaults_logic(app, current_cfg, vars_dict, populate_tree_func, load_weekdays_func=None):
    """
    Сброс к значениям SOURCE_FILE -> TARGET_FILE
    """
    # Ask for confirmation before resetting
    if not messagebox.askyesno(GUI_TEXT[153], GUI_TEXT[200], default=messagebox.NO):  # "Confirm", "Are you sure you want to reset..."
        return
    
    if os.path.exists(SOURCE_FILE):
        shutil.copy2(SOURCE_FILE, TARGET_FILE)
        reload_consts()
        current = _gather_current_config()
        _apply_to_consts(current)

        try:
            vars_dict["app_name_var"].set(current["app_name"])
        except Exception:
            pass
        try:
            vars_dict["app_size_var"].set(current["app_size"])
        except Exception:
            pass
        try:
            vars_dict["gui_lang_var"].set(current["GUI_LANGUAGE"])
        except Exception:
            pass
        try:
            vars_dict["afd_var"].set(current["autofill_direction"])
        except Exception:
            pass
        try:
            vars_dict["retries_var"].set(current["max_autofill_retries"])
        except Exception:
            pass
        try:
            vars_dict["lessons_var"].set(len(current.get("LESSONS", [])))
        except Exception:
            pass
        try:
            vars_dict.get("max_sequence_lessons_var").set(current.get("max_sequence_lessons", 2))
        except Exception:
            pass
        try:
            vars_dict.get("max_per_day_var").set(current.get("max_per_day", 3))
        except Exception:
            pass

        try:
            current_cfg.clear()
            current_cfg.update(current)
        except Exception:
            pass

        try:
            populate_tree_func()
        except Exception:
            pass
        if load_weekdays_func:
            try:
                load_weekdays_func()
            except Exception:
                pass

        messagebox.showinfo(GUI_TEXT[187], GUI_TEXT[191])  # "Config", "Reset to source_consts.py defaults."
    else:
        messagebox.showwarning(GUI_TEXT[187], GUI_TEXT[192])  # "Config", "source_consts.py not found."
