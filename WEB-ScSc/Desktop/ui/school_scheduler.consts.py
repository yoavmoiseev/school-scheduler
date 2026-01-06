import os


# ==========================================================

# === Auto-generated configuration file (consts.py) ===

# ==========================================================


LANGUAGES_LIST = ['English', 'Hebrew', 'Russian']

GUI_LANGUAGE = 'Hebrew'


TEXTS = {
  "English": {
    "app_name": "School Schedule Editor",
    "autofill_direction": "Left_to_Right",
    "weekdays": [
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


app_name = 'עורך מערכת שעות'

app_size = '1100x700'


max_autofill_retries = 15

autofill_direction = 'Right_to_Left'


BASE_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(BASE_DIR, 'data')

SCHEDULES_FILE = os.path.join(DATA_DIR, 'schedules.json')

SAVED_SCHEDULES_DIR = os.path.join(BASE_DIR, 'SAVED_SCHEDULES')


WEEKDAYS = ['יום שישי', 'יום חמישי', 'יום רביעי', 'יום שלישי', 'יום שני', 'יום ראשון']

LESSONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

TIME_SLOTS = {1: '09:15-10:00', 2: '10:00-10:40', 3: '10:45-11:30', 4: '11:30-12:15', 5: '12:20-13:00', 6: '14:00-14:45', 7: '14:55-15:40', 8: '15:50-16:35', 9: '16:40-17:25', 10: '17:30-18:15'}


unavailable_slot = 'XXXXXXXX'
