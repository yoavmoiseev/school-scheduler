import os
import sys


# ==========================================================
# === Auto-generated configuration file (consts.py) ===
# ==========================================================


LANGUAGES_LIST = ['English', 'Hebrew', 'Russian']
GUI_LANGUAGE = 'Russian'


TEXTS = {
  "English": {
    "app_name": "School Schedule Editor",
    "autofill_direction": "Left_to_Right",
    "weekdays": [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday"
    ]
  },
  "Hebrew": {
    "app_name": "עורך מערכת שעות",
    "autofill_direction": "Right_to_Left",
    "weekdays": [
      "יום שישי",
      "יום חמישי",
      "יום רביעי",
      "יום שלישי",
      "יום שני",
      "יום ראשון"
    ]
  },
  "Russian": {
    "app_name": "Редактор школьного расписания",
    "autofill_direction": "Left_to_Right",
    "weekdays": [
      "Понедельник",
      "Вторник",
      "Среда",
      "Четверг",
      "Пятница",
      "Суббота"
    ]
  }
}


app_name = 'School Schedule Editor'
app_size = '1500x900'


max_autofill_retries = 3
autofill_direction = 'Left_to_Right'


max_sequence_lessons = 2
max_per_day = 3


# ==========================================================
# === Directory Paths ===
# ==========================================================
# Detect if running as PyInstaller EXE or in development
if getattr(sys, 'frozen', False):
    # Running as compiled EXE - data folder is next to the EXE
    BASE_DIR = os.path.join(os.path.dirname(sys.executable), 'data')
else:
    # Running in development - data folder is current directory
    BASE_DIR = os.path.dirname(__file__)

DATA_DIR = BASE_DIR  # consts.py is already in data/ folder
SCHEDULES_FILE = os.path.join(DATA_DIR, 'schedules.json')
SAVED_SCHEDULES_DIR = os.path.join(DATA_DIR, 'SAVED_SCHEDULES')


WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
LESSONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
TIME_SLOTS = {1: '09:15-10:00', 2: '10:00-10:40', 3: '10:45-11:30', 4: '11:30-12:15', 5: '12:20-13:00', 6: '14:00-14:45', 7: '14:55-15:40', 8: '15:50-16:35', 9: '16:40-17:25', 10: '17:30-18:15'}


unavailable_slot = 'XXXXXXXX'

# ==== HIDDEN SECTION BELOW (do not modify) ====
# (used for detecting file changes)


__hidden_section_hash__ = 'e3b0c44298fc1c149af'
test = '4c8996fb92427ae41e4649b934ca495991b7852b855'


# ==== END OF HIDDEN SECTION ====
