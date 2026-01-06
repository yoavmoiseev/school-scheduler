# School Scheduler Web Application

A complete web-based school scheduling system with automatic schedule generation, Excel import/export, and multilingual support (English, Hebrew, Russian).

## Features

- **Multi-language Support**: English, Hebrew (עברית), Russian (Русский) with full RTL support
- **Teachers Management**: Add, edit, delete teachers with weekly hours and availability
- **Groups Management**: Organize students into groups
- **Subjects Management**: Define subjects with hours per week
- **Automatic Schedule Generation**: Intelligent autofill algorithm with conflict detection
- **Schedule Viewing**: View schedules by group or teacher
- **PDF Export**: Export schedules to PDF with WeasyPrint
- **Excel Integration**: Store all data in single Excel file (8 sheets)
- **Conflict Detection**: Prevents teacher double-booking
- **Constraints**: Configurable max consecutive lessons, max lessons per day
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, jQuery
- **Data Storage**: Excel (openpyxl)
- **PDF Generation**: ReportLab
- **Containerization**: Docker


## Быстрый старт на любом компьютере

1. Убедитесь, что установлен Python 3.7+ и добавлен в PATH.
2. После копирования проекта на новый компьютер запустите:
   ```
   setup.bat
   ```
   Этот скрипт автоматически создаст виртуальное окружение и установит все зависимости.
3. Для запуска приложения используйте:
   ```
   start.bat
   ```

## Project Structure

```
school_scheduler_web/
├── app.py                          # Flask application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker container definition
├── docker-compose.yml              # Docker Compose configuration
├── .env.example                    # Environment variables template
│
├── models/                         # Data models
│   ├── __init__.py
│   ├── teacher.py                  # Teacher class
│   ├── group.py                    # Group class
│   └── subject.py                  # Subject class
│
├── services/                       # Business logic
│   ├── __init__.py
│   ├── autofill_service.py         # Automatic schedule generation
│   ├── excel_service.py            # Excel I/O operations
│   ├── conflict_checker.py         # Teacher availability checking
│   ├── color_service.py            # Subject color generation
│   ├── pdf_service.py              # PDF export with ReportLab
│   └── i18n.py                     # Translations (200+ strings)
│
├── routes/                         # API endpoints
│   ├── __init__.py
│   ├── teachers.py                 # Teacher CRUD operations
│   ├── groups.py                   # Group CRUD operations
│   ├── subjects.py                 # Subject CRUD operations
│   ├── schedules.py                # Schedule operations
│   └── config_routes.py            # Configuration management
│
├── templates/                      # HTML templates
│   ├── base.html                   # Base layout
│   ├── index.html                  # Main page
│   └── components/
│       └── confirmations.html      # Modal dialogs
│
├── static/                         # Static assets
│   ├── css/
│   │   ├── custom.css              # Custom styles
│   │   └── schedule_grid.css       # Schedule grid styling
│   └── js/
│       ├── api_client.js           # API wrapper
│       ├── schedule_grid.js        # Grid rendering
│       ├── form_handlers.js        # Form logic
│       ├── confirmations.js        # Confirmation dialogs
│       └── i18n.js                 # Client-side translations
│
└── data/
    └── SchoolScheduler.xlsx        # Excel data file (created on first run)
```

## Installation

### Option 1: Local Installation

1. **Clone the repository** (or extract files)

2. **Install Python 3.10+**

3. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

4. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

7. **Open browser**: http://localhost:5000

### Option 2: Docker

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

2. **Open browser**: http://localhost:5000

3. **Stop the application**:
   ```bash
   docker-compose down
   ```

## Quick Start Guide

### 1. Add Teachers

- Go to **Teachers** tab
- Click **Add Teacher**
- Fill in:
  - Name
  - Subjects (add multiple with + button)
  - **Teachers Weekly Hours** (PRIORITY): `Monday:08:00-12:00; Monday:13:00-17:00`
  - Availability (fallback): `Monday:1-5; Tuesday:1-3`

**Important**: Teachers Weekly Hours takes priority over Availability!

### 2. Add Groups

- Go to **Groups** tab
- Click **Add Group**
- Enter group name (e.g., "Group A")

### 3. Add Subjects

- Go to **Subjects** tab
- Click **Add Subject**
- Fill in:
  - Subject name (e.g., "Math")
  - Group
  - Hours per week (e.g., 5)

### 4. Generate Schedule

- Go to **Group Scheduler** tab
- Select a group
- Click **Autofill**
- Confirm the action
- Schedule will be generated automatically!

### 5. View Teacher Schedules

- Go to **Teacher Scheduler** tab
- Select a teacher
- View their complete schedule (read-only)

### 6. Export to PDF

- In Group or Teacher Scheduler
- Click **Print to PDF**
- PDF will download automatically

## Configuration

Go to **General Configuration** tab to customize:

- **GUI Language**: English / עברית / Русский
- **Autofill Direction**: Forward / Backward / Random
- **Max Autofill Retries**: 100 (default)
- **Max Sequence Lessons**: 2 (max consecutive lessons of same subject)
- **Max Per Day**: 3 (max lessons of same subject per day)
- **Number of Lessons**: 8 (default)
- **Weekdays**: Monday,Tuesday,Wednesday,Thursday,Friday

## Excel File Format

The application uses a single Excel file (`data/SchoolScheduler.xlsx`) with 8 sheets:

### Sheet 1: Configuration
| Setting | Value |
|---------|-------|
| GUI_LANGUAGE | English |
| app_name | School Scheduler |
| lessons | 8 |
| max_sequence_lessons | 2 |
| max_per_day | 3 |
| max_autofill_retries | 100 |

### Sheet 4: Teachers (Example)
| Name | Subject | Hours | Group | Teachers Weekly Hours | Availability |
|------|---------|-------|-------|----------------------|--------------|
| John Smith | Math | 5 | Group A | Monday:08:00-12:00; Monday:13:00-17:00 | Monday:1-5 |

**Priority Logic**: If "Teachers Weekly Hours" is present, "Availability" is ignored. The system converts time ranges to lesson numbers automatically.

## API Endpoints

### Teachers
- `GET /api/teachers` - List all teachers
- `POST /api/teachers` - Create teacher
- `PUT /api/teachers/<name>` - Update teacher
- `DELETE /api/teachers/<name>` - Delete teacher

### Groups
- `GET /api/groups` - List all groups
- `POST /api/groups` - Create group
- `PUT /api/groups/<name>` - Update group
- `DELETE /api/groups/<name>` - Delete group

### Subjects
- `GET /api/subjects` - List all subjects
- `POST /api/subjects` - Create subject
- `PUT /api/subjects/<name>` - Update subject
- `DELETE /api/subjects/<name>` - Delete subject

### Schedules
- `GET /api/schedules/group/<group_name>` - Get group schedule
- `GET /api/schedules/teacher/<teacher_name>` - Get teacher schedule
- `POST /api/schedules/autofill` - Generate schedule automatically
- `POST /api/schedules/export-pdf` - Export to PDF
- `POST /api/schedules/clear` - Clear all schedules

### Configuration
- `GET /api/config` - Get configuration
- `POST /api/config` - Save configuration

## Autofill Algorithm

The automatic schedule generator:

1. **Reads** all teachers, subjects, and configuration
2. **Filters** subjects for the selected group
3. **Builds** teacher busy map from existing schedules
4. **Iterates** through each subject:
   - Finds available teacher
   - Checks teacher availability (weekly hours or availability slots)
   - Checks for conflicts (no double-booking)
   - Applies constraints (max consecutive, max per day)
   - Places lessons in optimal time slots
5. **Returns** complete schedule or error list

## Troubleshooting

### Application won't start
- Check Python version: `python --version` (need 3.10+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check if port 5000 is available

### Autofill fails
- Ensure teachers have availability defined
- Check that teachers teach the required subjects
- Increase `max_autofill_retries` in configuration
- Reduce `max_per_day` constraint

### PDF export fails
- On Windows, ReportLab should work without additional dependencies
- On Linux, ReportLab works out of the box
- Check that the `uploads` folder exists and is writable

### Excel file errors
- Delete `data/SchoolScheduler.xlsx` to regenerate with defaults
- Check file permissions

## Backup and Restore

There are server API endpoints and a local helper script to create and restore backups.

- Server API endpoints (when app is running):
   - `POST /api/admin/backup` — create a backup on the server (creates folder under `uploads/backups`)
   - `POST /api/admin/restore` — restore a named backup (JSON `{ "backup": "backup_YYYYMMDD_HHMMSS" }`)

- Local helper script: `scripts/backup_restore.py`
   - Create local zip backup: `python scripts/backup_restore.py backup`
   - List local backups: `python scripts/backup_restore.py list`
   - Restore local zip: `python scripts/backup_restore.py restore backups/backup_YYYYMMDD_HHMMSS.zip`
   - Use API backup: `python scripts/backup_restore.py api-backup --url http://localhost:5000`
   - Use API restore: `python scripts/backup_restore.py api-restore --url http://localhost:5000 --name backup_YYYYMMDD_HHMMSS`

The helper zips `data/` and `uploads/` into `backups/` by default.

## Development

### Running in debug mode
```python
# In app.py, last line:
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Adding new translations
Edit `services/i18n.py` and add to all three arrays:
- `GUI_TEXT` (English)
- `GUI_TEXT_HE` (Hebrew)
- `GUI_TEXT_RU` (Russian)

### Custom styling
Edit `static/css/custom.css` or `static/css/schedule_grid.css`

## Deployment

### Render.com

1. Push to GitHub
2. Create new Web Service on Render
3. Connect to your repository
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Deploy!

### Heroku

1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Deploy:
   ```bash
   git init
   heroku create
   git push heroku main
   ```

## License

MIT License

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Excel file format
3. Verify teacher availability configuration

## Credits

Converted from Tkinter desktop application to Flask web application.
