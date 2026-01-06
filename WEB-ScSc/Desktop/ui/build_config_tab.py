# build_config_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
from ui.global_config import _gather_current_config, _apply_to_consts, \
    ensure_consts_exist, reload_consts, save_consts_to_disk, consts, SOURCE_FILE, TARGET_FILE
import ui.translations as tr


def _tr(text):
    """Return localized string by finding English key index in translations.
    Falls back to original text if not found.
    """
    try:
        idx = tr.ENGLISH.index(text)
        return tr.GUI_TEXT[idx]
    except Exception:
        return text

# импорт логики
from ui.config_tab_logic import (
    populate_tree, add_or_update_slot, delete_slot,
    on_save_logic, on_reload_logic, on_reset_defaults_logic
)

# build_config_tab.py
def build_config_tab(app, parent_frame):
    """
    Build 'General Configuration' UI inside parent_frame.
    app: main application instance
    parent_frame: tk.Frame
    """
    ensure_consts_exist()
    reload_consts()

    current_cfg = _gather_current_config()
    _apply_to_consts(current_cfg)

    frm = parent_frame

    # === Tab visibility handlers =======================================
    # Warning removed - no longer needed with full restart functionality
    
    # ================================
    # PARENT COLUMN CONFIGURATION
    # ================================
    frm.columnconfigure(0, weight=0)
    frm.columnconfigure(1, weight=0)
    frm.columnconfigure(2, weight=0)

    # ================================
    # MIDDLE COLUMN FRAME
    # ================================
    middle_column = tk.Frame(frm)
    middle_column.grid(
        row=0,
        column=2,
        rowspan=999,
        sticky="w",
        pady=20,
        padx=50
    )

    # ================================
    # RIGHT COLUMN FRAME
    # ================================
    right_column = tk.Frame(frm)
    right_column.grid(
        row=0,
        column=3,
        rowspan=999,
        sticky="nw",
        pady=20,
        padx=150
    )

    row = 0

    # === Top basic settings (kept exactly same functionality) ===
    tk.Label(frm, text=_tr("Application title:")).grid(row=row, column=0, sticky="w", padx=6, pady=6)
    app_name_var = tk.StringVar(value=current_cfg["app_name"])
    tk.Entry(frm, textvariable=app_name_var).grid(row=row, column=1, sticky="ew", padx=6, pady=6)
    row += 1

    tk.Label(frm, text=_tr("Window size (WxH):")).grid(row=row, column=0, sticky="w", padx=6, pady=6)
    app_size_var = tk.StringVar(value=current_cfg["app_size"])
    tk.Entry(frm, textvariable=app_size_var).grid(row=row, column=1, sticky="w", padx=6, pady=6)
    row += 1

    tk.Label(frm, text=_tr("GUI language:")).grid(row=row, column=0, sticky="w", padx=6, pady=6)
    gui_lang_var = tk.StringVar(value=current_cfg["GUI_LANGUAGE"])
    langs = current_cfg["LANGUAGES_LIST"]
    lang_cb = ttk.Combobox(frm, values=langs, textvariable=gui_lang_var, state="readonly", width=20)
    lang_cb.grid(row=row, column=1, sticky="w", padx=6, pady=6)
    row += 1

    tk.Label(frm, text=_tr("Autofill direction:")).grid(row=row, column=0, sticky="w", padx=6, pady=6)
    afd_var = tk.StringVar(value=current_cfg["autofill_direction"])
    afd_cb = ttk.Combobox(frm, values=["Left_to_Right", "Right_to_Left"], textvariable=afd_var, state="readonly", width=20)
    afd_cb.grid(row=row, column=1, sticky="w", padx=6, pady=6)
    row += 1

    tk.Label(frm, text=_tr("Max autofill retries:")).grid(row=row, column=0, sticky="w", padx=6, pady=6)
    retries_var = tk.IntVar(value=current_cfg["max_autofill_retries"])
    tk.Spinbox(frm, from_=0, to=100, textvariable=retries_var, width=6).grid(row=row, column=1, sticky="w", padx=6, pady=6)
    row += 1

    #=========================================================
    # === LESSONS and TIME_SLOTS Editing ===
    #=========================================================

    tk.Label(frm, text=_tr("Number of lessons:")).grid(row=row, column=0, sticky="w", padx=6, pady=6)
    lessons_var = tk.IntVar(value=len(current_cfg.get("LESSONS", [])))
    lessons_spin = tk.Spinbox(frm, from_=1, to=20, textvariable=lessons_var, width=6)
    lessons_spin.grid(row=row, column=1, sticky="w", padx=6, pady=6)
    row += 1

    # TIME_SLOTS: Treeview for visual editing
    tk.Label(frm, text=_tr("Time slots:")).grid(row=row, column=0, sticky="nw", padx=4, pady=4)

    # Frame for time slots (fixed size, not stretchable)
    slots_frame = tk.Frame(frm, width=300, height=300, relief="groove", borderwidth=1)
    slots_frame.grid(row=row, column=1, sticky="nw", padx=4, pady=4)
    slots_frame.grid_propagate(True)

    cols = ("lesson", "time")
    tree = ttk.Treeview(slots_frame, columns=cols, show="headings", height=10)
    tree.heading("lesson", text=_tr("Lesson"))
    tree.heading("time", text=_tr("Time range"))
    tree.column("lesson", width=60, anchor="w")
    tree.column("time", width=120, anchor="w")
    tree.grid(row=0, column=0, sticky="nw")

    scrollbar = ttk.Scrollbar(slots_frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="nsw")
    tree.configure(yscrollcommand=scrollbar.set)

    # populate tree — теперь через обёртку, которая вызывает логику
    def populate_tree_func():
        populate_tree(tree, lessons_var, current_cfg)

    populate_tree_func()

    # editing controls under tree
    edit_fr = tk.Frame(slots_frame)
    edit_fr.grid(row=1, column=0, columnspan=2, sticky="w", pady=4)

    tk.Label(edit_fr, text=_tr("L:")).grid(row=0, column=0, sticky="w")
    edit_lesson_var = tk.IntVar(value=1)
    tk.Spinbox(edit_fr, from_=1, to=30, textvariable=edit_lesson_var, width=3).grid(row=0, column=1, sticky="w")

    tk.Label(edit_fr, text=_tr("T:")).grid(row=0, column=2, sticky="w", padx=(6,0))
    edit_time_var = tk.StringVar()
    tk.Entry(edit_fr, textvariable=edit_time_var, width=10).grid(row=0, column=3, sticky="w", padx=2)

    # on_select_tree остаётся UI (работает с виджетами)
    def on_select_tree(event):
        sel = tree.selection()
        if not sel:
            return
        iid = sel[0]
        vals = tree.item(iid, "values")
        try:
            edit_lesson_var.set(int(vals[0]))
        except Exception:
            pass
        edit_time_var.set(vals[1])

    tree.bind("<<TreeviewSelect>>", on_select_tree)

    # кнопки + / - вызывают логику через обёртки
    def add_slot_wrapper():
        add_or_update_slot(tree, edit_lesson_var, edit_time_var)

    def delete_slot_wrapper():
        delete_slot(tree, edit_lesson_var)

    tk.Button(edit_fr, text="+", command=add_slot_wrapper, width=2).grid(row=0, column=4, padx=3)
    tk.Button(edit_fr, text="-", command=delete_slot_wrapper, width=2).grid(row=0, column=5, padx=3)

    # when lessons count changes
    def on_lessons_change(*_):
        try:
            v = int(lessons_var.get())
        except Exception:
            v = len(current_cfg.get("LESSONS", []))
        current_cfg["LESSONS"] = list(range(1, v + 1))
        populate_tree_func()

    lessons_var.trace_add("write", lambda *_: on_lessons_change())

    # ---------------------------------------------------------
    # WEEKDAYS block- according to language selected, Edit button under it
    # ---------------------------------------------------------
    
    tk.Label(frm, text=_tr("Edit weekdays:")).grid(row=row, column=0, sticky="nw", padx=6, pady=40)

    weekdays_txt = tk.Text(frm, height=7, width=15, wrap="none", relief="groove", borderwidth=3)
    weekdays_txt.grid(row=row, column=0, padx=6, pady=73)

    def warn(e):
        messagebox.showinfo(_tr("Info"), _tr("If you edit weekdays — all data must be manually reentered! Use keyboard for editing, one day per line."))

    weekdays_txt.bind("<Button-1>", warn)

    

    # ========================================================================================
    # === Load weekdays for selected language function ===
    def load_weekdays_for_selected_lang(*_):
        sel = gui_lang_var.get()
        days = consts.TEXTS.get(sel, {}).get("weekdays", [])
        weekdays_txt.delete("1.0", tk.END)
        weekdays_txt.insert("1.0", "\n".join(days))

    lang_cb.bind("<<ComboboxSelected>>", load_weekdays_for_selected_lang)
    load_weekdays_for_selected_lang()

    # ==========================================================
    # === Button Handlers: Save, Reload, Reset (делегируем логике)
    # ==========================================================
    


    # Save -> вызывает on_save_logic из config_tab_logic.py
    def on_save():
        on_save_logic(app, current_cfg, vars_dict, tree, weekdays_txt)

    def on_reload():
        # вызываем логику и просим её также обновить weekdays
        on_reload_logic(app, current_cfg, vars_dict, populate_tree_func, load_weekdays_for_selected_lang)

    def on_reset_defaults():
        on_reset_defaults_logic(app, current_cfg, vars_dict, populate_tree_func, load_weekdays_for_selected_lang)

    # ================================
    # MIDDLE COLUMN BUTTONS (visually emphasized)
    # ================================
    tk.Button(
        middle_column,
        text=_tr("Save"),
        command=on_save,
        font=("Arial", 12, "bold")
    ).pack(pady=10, padx=20)

    tk.Button(
        middle_column,
        text=_tr("Reload last saved"),
        command=on_reload,
        font=("Arial", 12, "bold")
    ).pack(pady=10, padx=20)

    tk.Button(
        middle_column,
        text=_tr("Reset to defaults"),
        command=on_reset_defaults,
        font=("Arial", 12, "bold")
    ).pack(pady=10, padx=20)

    # ====================================================================================
    # === RIGHT column (placed in parent column 2) =======================================
    # ====================================================================================
  
    # Scheduling limits (from source_consts / consts)
    row += 1
    tk.Label(right_column, text=_tr("Max sequence lessons:")).grid(row=row, column=0, sticky="w", padx=6, pady=6)
    max_sequence_lessons_var = tk.IntVar(value=current_cfg.get("max_sequence_lessons", 2))
    tk.Spinbox(right_column, from_=0, to=20, textvariable=max_sequence_lessons_var, width=6).grid(row=row, column=1, sticky="w", padx=6, pady=6)
    row += 1
    tk.Label(right_column, text=_tr("Max lessons per day:")).grid(row=row, column=0, sticky="w", padx=6, pady=6)
    max_per_day_var = tk.IntVar(value=current_cfg.get("max_per_day", 3))
    tk.Spinbox(right_column, from_=0, to=20, textvariable=max_per_day_var, width=6).grid(row=row, column=1, sticky="w", padx=6, pady=6)
    row += 1

    # ====================================================================================
    vars_dict = {
        "app_name_var": app_name_var,
        "app_size_var": app_size_var,
        "gui_lang_var": gui_lang_var,
        "afd_var": afd_var,
        "retries_var": retries_var,
        "lessons_var": lessons_var,
        "max_sequence_lessons_var": max_sequence_lessons_var,
        "max_per_day_var": max_per_day_var,
    }
    
    # ====================================================================================

    app.config_widgets = {
        "app_name_var": app_name_var,
        "app_size_var": app_size_var,
        "gui_lang_var": gui_lang_var,
        "afd_var": afd_var,
        "retries_var": retries_var,
        "weekdays_txt": weekdays_txt,
        "lessons_var": lessons_var,
        "time_slots_tree": tree,
        "max_sequence_lessons_var": max_sequence_lessons_var,
        "max_per_day_var": max_per_day_var,
    }

    return frm
