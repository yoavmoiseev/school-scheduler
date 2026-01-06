# school_scheduler/ui/global_config.py
# tab that concentrates general configuration options (ENHANCED)
import os
import shutil
import importlib
import tkinter as tk
from tkinter import ttk, messagebox
import json

import school_scheduler.data.consts as consts
from school_scheduler.ui.translations import GUI_TEXT

# Use DATA_DIR from consts which correctly handles frozen/dev modes
DATA_DIR = consts.DATA_DIR

SOURCE_FILE = os.path.join(DATA_DIR, "source_consts.py")
TARGET_FILE = os.path.join(DATA_DIR, "consts.py")

# ==========================================================
# === Ensure consts.py exists (copy from source if needed)
# ==========================================================
def ensure_consts_exist():
    """If consts.py missing, copy from source_consts.py"""
    if not os.path.exists(TARGET_FILE):
        if os.path.exists(SOURCE_FILE):
            shutil.copy2(SOURCE_FILE, TARGET_FILE)
        else:
            messagebox.showerror(GUI_TEXT[67], GUI_TEXT[193])  # "Error", "Neither consts.py nor source_consts.py found."


# ==========================================================
# === Reload constants dynamically
# ==========================================================
def reload_consts():
    """Reload consts module dynamically - force load from external file"""
    ensure_consts_exist()
    
    # Force reload from external file (not from EXE archive)
    if os.path.exists(TARGET_FILE):
        with open(TARGET_FILE, 'r', encoding='utf-8') as f:
            code = f.read()
        # Execute in consts module namespace to update it
        exec(code, consts.__dict__)
    else:
        # Fallback to normal reload
        importlib.reload(consts)
    
    return consts


# ==========================================================
# === Apply dict to consts.py (in memory)
# ==========================================================
def _apply_to_consts(cfg: dict):
    """Apply configuration dict to in-memory consts"""
    if "GUI_LANGUAGE" in cfg:
        try:
            consts.GUI_LANGUAGE = cfg["GUI_LANGUAGE"]
        except Exception:
            pass

    for key in ("app_name", "app_size"):
        if key in cfg:
            try:
                setattr(consts, key, cfg[key])
            except Exception:
                pass

    if "max_autofill_retries" in cfg:
        try:
            consts.max_autofill_retries = int(cfg["max_autofill_retries"])
        except Exception:
            pass

    if "max_sequence_lessons" in cfg:
        try:
            consts.max_sequence_lessons = int(cfg["max_sequence_lessons"])
        except Exception:
            pass

    if "max_per_day" in cfg:
        try:
            consts.max_per_day = int(cfg["max_per_day"])
        except Exception:
            pass

    if "autofill_direction" in cfg:
        try:
            consts.autofill_direction = cfg["autofill_direction"]
        except Exception:
            pass

    # LESSONS and TIME_SLOTS
    if "LESSONS" in cfg:
        try:
            consts.LESSONS = cfg["LESSONS"]
        except Exception:
            pass

    if "TIME_SLOTS" in cfg:
        try:
            consts.TIME_SLOTS = cfg["TIME_SLOTS"]
        except Exception:
            pass

    # Update TEXTS if provided
    if "TEXTS" in cfg and isinstance(cfg["TEXTS"], dict):
        try:
            consts.TEXTS = cfg["TEXTS"]
        except Exception:
            pass

    # Update weekdays
    try:
        if hasattr(consts, "TEXTS") and consts.GUI_LANGUAGE in consts.TEXTS:
            consts.WEEKDAYS = consts.TEXTS[consts.GUI_LANGUAGE].get("weekdays", consts.WEEKDAYS)
    except Exception:
        pass

    # Hidden/internal vars
    if "HIDDEN" in cfg and isinstance(cfg["HIDDEN"], dict):
        try:
            consts.HIDDEN = cfg["HIDDEN"]
        except Exception:
            pass


# ==========================================================
# === Gather current config into dict
# ==========================================================
def _gather_current_config():
    """Create serializable dict from current consts"""
    cfg = {}
    cfg["LANGUAGES_LIST"] = getattr(consts, "LANGUAGES_LIST", ["English", "Hebrew", "Russian"])
    cfg["GUI_LANGUAGE"] = getattr(consts, "GUI_LANGUAGE", "English")
    cfg["TEXTS"] = getattr(consts, "TEXTS", {})
    cfg["app_name"] = getattr(consts, "app_name", "")
    cfg["app_size"] = getattr(consts, "app_size", "")
    cfg["max_autofill_retries"] = getattr(consts, "max_autofill_retries", 15)
    cfg["autofill_direction"] = getattr(consts, "autofill_direction", "Left_to_Right")
    cfg["max_sequence_lessons"] = getattr(consts, "max_sequence_lessons", 2)
    cfg["max_per_day"] = getattr(consts, "max_per_day", 3)
    cfg["WEEKDAYS"] = getattr(consts, "WEEKDAYS", [])
    cfg["LESSONS"] = getattr(consts, "LESSONS", list(range(1, 11)))
    cfg["TIME_SLOTS"] = getattr(consts, "TIME_SLOTS", {})
    cfg["unavailable_slot"] = getattr(consts, "unavailable_slot", "XXXXXXXX")
    cfg["HIDDEN"] = getattr(consts, "HIDDEN", {})  # hidden/internal vars preserved but not shown
    return cfg


# ==========================================================
# === Save updated config directly into consts.py
# ==========================================================
def save_consts_to_disk(cfg: dict):
    """Rewrite consts.py file with updated configuration (preserves hidden vars)"""
    ensure_consts_exist()
    try:
        lines = []
        lines.append("import os")
        lines.append("import sys\n\n")
        lines.append("# ==========================================================")
        lines.append("# === Auto-generated configuration file (consts.py) ===")
        lines.append("# ==========================================================\n\n")

        # Languages
        langs = cfg.get("LANGUAGES_LIST", ["English", "Hebrew", "Russian"])
        lines.append(f"LANGUAGES_LIST = {repr(langs)}")
        lines.append(f"GUI_LANGUAGE = {repr(cfg.get('GUI_LANGUAGE', 'English'))}\n\n")

        # TEXTS (as readable JSON-like structure)
        texts_str = json.dumps(cfg.get("TEXTS", {}), ensure_ascii=False, indent=2)
        lines.append("TEXTS = " + texts_str + "\n\n")

        # App info
        lines.append(f"app_name = {repr(cfg.get('app_name', 'School Schedule Editor'))}")
        lines.append(f"app_size = {repr(cfg.get('app_size', '1100x700'))}\n\n")

        # Autofill
        lines.append(f"max_autofill_retries = {int(cfg.get('max_autofill_retries', 15))}")
        lines.append(f"autofill_direction = {repr(cfg.get('autofill_direction', 'Left_to_Right'))}\n\n")

        # scheduling limits
        lines.append(f"max_sequence_lessons = {int(cfg.get('max_sequence_lessons', 2))}")
        lines.append(f"max_per_day = {int(cfg.get('max_per_day', 3))}\n\n")

        # Paths - with frozen mode detection
        lines.append("# ==========================================================")
        lines.append("# === Directory Paths ===")
        lines.append("# ==========================================================")
        lines.append("# Detect if running as PyInstaller EXE or in development")
        lines.append("if getattr(sys, 'frozen', False):")
        lines.append("    # Running as compiled EXE - data folder is next to the EXE")
        lines.append("    BASE_DIR = os.path.join(os.path.dirname(sys.executable), 'data')")
        lines.append("else:")
        lines.append("    # Running in development - data folder is current directory")
        lines.append("    BASE_DIR = os.path.dirname(__file__)")
        lines.append("")
        lines.append("DATA_DIR = BASE_DIR  # consts.py is already in data/ folder")
        lines.append("SCHEDULES_FILE = os.path.join(DATA_DIR, 'schedules.json')")
        lines.append("SAVED_SCHEDULES_DIR = os.path.join(DATA_DIR, 'SAVED_SCHEDULES')\n\n")

        # UI / Domain Constants
        lines.append(f"WEEKDAYS = {repr(cfg.get('WEEKDAYS', []))}")
        lines.append(f"LESSONS = {repr(cfg.get('LESSONS', list(range(1, 11))))}")
        lines.append(f"TIME_SLOTS = {repr(cfg.get('TIME_SLOTS', {}))}\n\n")

        # Tokens
        lines.append(f"unavailable_slot = {repr(cfg.get('unavailable_slot', 'XXXXXXXX'))}\n\n")

        # Hidden/internal vars (preserve at end, but don't show in UI)
        hidden = cfg.get('HIDDEN', {})
        if hidden:
            lines.append("# ==========================================================")
            lines.append("# === Hidden/Internal Constants (preserved) ===")
            lines.append("# ==========================================================\n")
            for k, v in hidden.items():
                lines.append(f"{k} = {repr(v)}")

        # === preserve user section ===
        marker = "# ==== HIDDEN SECTION BELOW (do not modify) ===="
        hidden_part = ""

        if os.path.exists(TARGET_FILE):
            with open(TARGET_FILE, "r", encoding="utf-8") as f:
                old_data = f.read()
                if marker in old_data:
                    hidden_part = old_data.split(marker, 1)[1]

        # ---- write combined data once ----
        new_data = "\n".join(lines).strip()
        with open(TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(new_data + "\n\n" + marker + hidden_part)

        # Reload immediately from external file
        reload_consts()
        return True

    except Exception as e:
        print("Error saving consts.py:", e)
        return False

