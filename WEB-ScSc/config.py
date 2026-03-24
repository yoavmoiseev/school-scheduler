import os
import sys

def _get_base_dir():
    """Return the writable base directory: exe folder when frozen, project folder otherwise."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

_BASE_DIR = _get_base_dir()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    EXCEL_FILE = os.path.join(_BASE_DIR, 'data', 'SchoolScheduler.xlsx')
    UPLOAD_FOLDER = os.path.join(_BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # From source_consts.py
    LANGUAGES_LIST = ['English', 'Hebrew', 'Russian']
    DEFAULT_LANGUAGE = 'English'
    APP_NAME = 'School Schedule Editor'
    APP_SIZE = '1500x900'
    MAX_AUTOFILL_RETRIES = 2
    AUTOFILL_DIRECTION = 'Left_to_Right'
    MAX_SEQUENCE_LESSONS = 2
    MAX_PER_DAY = 3
    LESSONS = 10
    UNAVAILABLE_SLOT = 'XXXXXXXX'
    
    # Time slots from source_consts.py
    TIME_SLOTS = {
        1: '09:15-10:00',
        2: '10:00-10:40',
        3: '10:45-11:30',
        4: '11:30-12:15',
        5: '12:20-13:00',
        6: '14:00-14:45',
        7: '14:55-15:40',
        8: '15:50-16:35',
        9: '16:40-17:25',
        10: '17:30-18:15'
    }
    
    # Weekdays from source_consts.py
    WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
