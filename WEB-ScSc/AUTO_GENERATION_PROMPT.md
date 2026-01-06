# AUTO-GENERATION PROMPT FOR WEB VERSION
# Use this with Claude, GPT-4, or other AI code generator

---

## CONTEXT

You are converting a **Tkinter desktop application** (School Scheduler) to a **Flask + Bootstrap 5 web application**. The original app is 4,000 lines of Python code with complete scheduling logic, Excel import/export, and multilingual support (English/Hebrew/Russian).

**Goal**: Create a PIXEL-PERFECT web version that preserves 100% of functionality.

**Source Documentation**: See `WEB_CONVERSION_SPEC.md` for complete UI/functionality specification.

---

## YOUR TASK

Generate a complete, production-ready Flask web application with the following structure:

```
school_scheduler_web/
├── app.py                          # Flask app (routes + initialization)
├── requirements.txt                # Dependencies
├── config.py                       # Flask configuration
├── README.md                       # Setup instructions
├── Dockerfile                      # Docker container
├── docker-compose.yml              # Docker Compose setup
├── .env.example                    # Environment variables template
│
├── models/                         # Data models (REUSE FROM SOURCE)
│   ├── __init__.py
│   ├── teacher.py                  # Teacher class
│   ├── group.py                    # Group class
│   └── subject.py                  # Subject class
│
├── services/                       # Business logic (REUSE FROM SOURCE)
│   ├── __init__.py
│   ├── autofill_service.py         # Autofill algorithm (app_core.py L341-540)
│   ├── excel_service.py            # Excel I/O (buttons_functions.py L321-814)
│   ├── conflict_checker.py         # Teacher busy map (teacher_busy_map.py)
│   ├── schedule_service.py         # Schedule CRUD operations
│   ├── data_utils.py               # Data normalization (data_utils.py)
│   ├── i18n.py                     # Translations (translations.py - all 670 lines)
│   ├── pdf_service.py              # PDF export with WeasyPrint
│   └── color_service.py            # Color generation (ui_helpers.py L37-55)
│
├── routes/                         # API endpoints
│   ├── __init__.py
│   ├── teachers.py                 # /api/teachers/* endpoints
│   ├── groups.py                   # /api/groups/* endpoints
│   ├── subjects.py                 # /api/subjects/* endpoints
│   ├── schedules.py                # /api/schedules/* endpoints
│   ├── config.py                   # /api/config/* endpoints
│   └── import_export.py            # /api/import, /api/export
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                   # Base layout (navbar, tabs, footer)
│   ├── index.html                  # Home page (top toolbar)
│   ├── teachers/
│   │   ├── list.html               # Teachers table
│   │   └── edit_modal.html         # Edit teacher modal
│   ├── groups/
│   │   ├── list.html               # Groups table
│   │   └── edit_modal.html         # Edit group modal
│   ├── subjects/
│   │   ├── list.html               # Subjects table
│   │   └── edit_modal.html         # Edit subject modal
│   ├── schedules/
│   │   ├── day_view.html           # Day schedule grid
│   │   ├── group_scheduler.html    # Group schedule grid + autofill
│   │   ├── teacher_scheduler.html  # Teacher schedule grid (read-only)
│   │   └── lesson_modal.html       # Add/Edit lesson modal
│   ├── configuration/
│   │   └── settings.html           # Configuration form (3 columns)
│   └── components/
│       ├── toolbar.html            # Top 12 buttons
│       ├── tabs.html               # Tab navigation
│       └── confirmations.html      # Confirmation modals
│
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css       # Bootstrap 5.3
│   │   ├── custom.css              # Custom styles (grids, colors, RTL)
│   │   └── schedule_grid.css       # Schedule grid styling
│   ├── js/
│   │   ├── bootstrap.bundle.min.js # Bootstrap JS
│   │   ├── jquery.min.js           # jQuery 3.6
│   │   ├── api_client.js           # API wrapper functions
│   │   ├── schedule_grid.js        # Grid rendering + interactions
│   │   ├── form_handlers.js        # Form validation + submission
│   │   ├── confirmations.js        # Confirmation dialogs (default: NO)
│   │   └── i18n.js                 # Client-side translations
│   └── img/
│       └── logo.png                # App logo
│
├── data/
│   └── SchoolScheduler.xlsx        # Single Excel file (8 sheets)
│
└── tests/                          # Unit tests
    ├── test_autofill.py
    ├── test_excel_io.py
    ├── test_conflicts.py
    └── test_api.py
```

---

## DETAILED REQUIREMENTS

### 1. DATA STORAGE (EXCEL FILE)

**File**: `data/SchoolScheduler.xlsx`

**Sheet 1: Configuration**
| Setting | Value |
|---------|-------|
| GUI_LANGUAGE | English |
| app_name | School Scheduler |
| app_size | 1400x900 |
| autofill_direction | forward |
| max_autofill_retries | 100 |
| max_sequence_lessons | 2 |
| max_per_day | 3 |

**Sheet 2: Weekdays**
| Order | Weekday | Short |
|-------|---------|-------|
| 1 | Monday | M |
| 2 | Tuesday | T |
| ... | ... | ... |

**Sheet 3: Time Slots**
| Lesson | Time Range |
|--------|------------|
| 1 | 08:00-09:00 |
| 2 | 09:00-10:00 |
| ... | ... |

**Sheet 4: Teachers**
| Name | Subject | Hours | Group | Teachers Weekly Hours | Availability |
|------|---------|-------|-------|----------------------|--------------|
| John Smith | Math | 5 | Group A | Monday:08:00-12:00; Monday:13:00-17:00 | Monday:1-5; Tuesday:1-3 |

**CRITICAL**: Teachers Weekly Hours column is THE PRIORITY. If present, ignore Availability.

**Sheet 5-8**: Groups, Subjects, Group Schedules, Teacher Schedules

**Implementation**:
```python
# services/excel_service.py
import openpyxl
from openpyxl import Workbook, load_workbook

class ExcelService:
    def __init__(self, file_path='data/SchoolScheduler.xlsx'):
        self.file_path = file_path
        self.wb = None
    
    def load(self):
        """Load Excel file or create if not exists"""
        if os.path.exists(self.file_path):
            self.wb = load_workbook(self.file_path)
        else:
            self._create_default()
    
    def get_config(self):
        """Read Configuration sheet"""
        sheet = self.wb['Configuration']
        config = {}
        for row in sheet.iter_rows(min_row=2, values_only=True):
            config[row[0]] = row[1]
        return config
    
    def get_teachers(self):
        """Read Teachers sheet with PRIORITY logic"""
        sheet = self.wb['Teachers']
        teachers = {}
        for row in sheet.iter_rows(min_row=2, values_only=True):
            name, subject, hours, group, weekly_hours, availability = row
            
            if name not in teachers:
                teachers[name] = {
                    'name': name,
                    'subjects': [],
                    'available_slots': {},
                    'check_in_hours': {},
                    'check_out_hours': {}
                }
            
            teachers[name]['subjects'].append({
                'name': subject,
                'hours': hours,
                'group': group
            })
            
            # PRIORITY: Teachers Weekly Hours > Availability
            if weekly_hours:
                check_in, check_out = self._parse_weekly_hours(weekly_hours)
                teachers[name]['check_in_hours'] = check_in
                teachers[name]['check_out_hours'] = check_out
                # Recalculate available_slots from times
                time_slots = self.get_time_slots()
                teachers[name]['available_slots'] = self._convert_times_to_lessons(
                    check_in, check_out, time_slots
                )
            elif availability:
                teachers[name]['available_slots'] = self._parse_availability(availability)
        
        return list(teachers.values())
    
    def _parse_weekly_hours(self, weekly_hours_str):
        """
        Parse: "Monday:08:00-12:00; Monday:13:00-17:00; Tuesday:09:00-15:00"
        Returns: ({Monday: ['08:00', '13:00'], Tuesday: ['09:00']}, 
                  {Monday: ['12:00', '17:00'], Tuesday: ['15:00']})
        """
        check_in = {}
        check_out = {}
        
        for entry in weekly_hours_str.split(';'):
            entry = entry.strip()
            if not entry:
                continue
            day, time_range = entry.split(':')
            start, end = time_range.split('-')
            
            if day not in check_in:
                check_in[day] = []
                check_out[day] = []
            
            check_in[day].append(start)
            check_out[day].append(end)
        
        return check_in, check_out
    
    def _convert_times_to_lessons(self, check_in, check_out, time_slots):
        """Convert HH:MM ranges to lesson numbers using TIME_SLOTS"""
        available_slots = {}
        
        for day in check_in:
            available_slots[day] = []
            
            for start_time, end_time in zip(check_in[day], check_out[day]):
                for lesson_num, time_range in time_slots.items():
                    slot_start, slot_end = time_range.split('-')
                    if start_time <= slot_start < end_time:
                        available_slots[day].append(lesson_num)
        
        return available_slots
    
    def save(self):
        """Save Excel file"""
        self.wb.save(self.file_path)
```

---

### 2. AUTOFILL ALGORITHM (CRITICAL)

**Source**: `app_core.py` lines 341-540

**Port to**: `services/autofill_service.py`

```python
class AutofillService:
    def __init__(self, excel_service, conflict_checker):
        self.excel = excel_service
        self.checker = conflict_checker
    
    def autofill_group(self, group_name, max_retries=100):
        """
        Autofill schedule for a group.
        Returns: (success: bool, schedule: dict, errors: list)
        """
        config = self.excel.get_config()
        teachers = self.excel.get_teachers()
        subjects = self.excel.get_subjects()
        weekdays = config['WEEKDAYS'].split(',')
        lessons = list(range(1, int(config['lessons']) + 1))
        
        # Filter subjects for this group
        group_subjects = [s for s in subjects if s['group'] == group_name]
        
        # Initialize schedule
        schedule = {}
        for day in weekdays:
            schedule[day] = {}
        
        # Build teacher busy map
        existing_schedules = self.excel.get_group_schedules()
        busy_map = self.checker.build_busy_map(existing_schedules, teachers)
        
        errors = []
        
        # For each subject
        for subject in group_subjects:
            # Find teacher
            teacher = self._find_teacher(subject, teachers)
            if not teacher:
                errors.append(f"No teacher for {subject['name']}")
                continue
            
            # Calculate required lessons
            required = subject['hours_per_week']
            placed = 0
            retries = 0
            
            # Place lessons
            while placed < required and retries < max_retries:
                for day in weekdays:
                    for lesson in lessons:
                        # Check availability
                        if lesson not in teacher.get('available_slots', {}).get(day, []):
                            continue
                        
                        # Check conflicts
                        if self.checker.is_busy(busy_map, teacher['name'], day, lesson):
                            continue
                        
                        # Check constraints
                        if not self._check_constraints(schedule, day, lesson, subject, config):
                            continue
                        
                        # Place lesson
                        schedule[day][lesson] = {
                            'subject': subject['name'],
                            'teacher': teacher['name'],
                            'group': group_name,
                            'color_bg': self._get_color(subject['name']),
                            'color_fg': '#000000'
                        }
                        
                        # Update busy map
                        busy_map[teacher['name']][day][lesson] = True
                        placed += 1
                        
                        if placed >= required:
                            break
                    
                    if placed >= required:
                        break
                
                retries += 1
            
            if placed < required:
                errors.append(f"Could not place all hours for {subject['name']} (placed {placed}/{required})")
        
        return (len(errors) == 0, schedule, errors)
    
    def _check_constraints(self, schedule, day, lesson, subject, config):
        """Check max_sequence_lessons and max_per_day constraints"""
        max_sequence = int(config.get('max_sequence_lessons', 2))
        max_per_day = int(config.get('max_per_day', 3))
        
        # Check sequence
        sequence_count = 0
        for i in range(lesson - max_sequence, lesson):
            if i in schedule.get(day, {}) and schedule[day][i]['subject'] == subject['name']:
                sequence_count += 1
        if sequence_count >= max_sequence:
            return False
        
        # Check daily limit
        day_count = sum(1 for l in schedule.get(day, {}).values() if l['subject'] == subject['name'])
        if day_count >= max_per_day:
            return False
        
        return True
```

---

### 3. API ENDPOINTS

**routes/teachers.py**:
```python
from flask import Blueprint, request, jsonify

teachers_bp = Blueprint('teachers', __name__)

@teachers_bp.route('/api/teachers', methods=['GET'])
def get_teachers():
    """List all teachers"""
    teachers = excel_service.get_teachers()
    return jsonify(teachers)

@teachers_bp.route('/api/teachers', methods=['POST'])
def create_teacher():
    """Create new teacher"""
    data = request.json
    # Validate
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400
    
    # Add to Excel
    excel_service.add_teacher(data)
    return jsonify({'success': True, 'teacher': data}), 201

@teachers_bp.route('/api/teachers/<name>', methods=['GET'])
def get_teacher(name):
    """Get teacher details"""
    teacher = excel_service.get_teacher(name)
    if not teacher:
        return jsonify({'error': 'Teacher not found'}), 404
    return jsonify(teacher)

@teachers_bp.route('/api/teachers/<name>', methods=['PUT'])
def update_teacher(name):
    """Update teacher"""
    data = request.json
    success = excel_service.update_teacher(name, data)
    if not success:
        return jsonify({'error': 'Teacher not found'}), 404
    return jsonify({'success': True})

@teachers_bp.route('/api/teachers/<name>', methods=['DELETE'])
def delete_teacher(name):
    """Delete teacher"""
    success = excel_service.delete_teacher(name)
    if not success:
        return jsonify({'error': 'Teacher not found'}), 404
    return jsonify({'success': True})
```

**Similar for**: groups.py, subjects.py, schedules.py, config.py

---

### 4. FRONTEND (BOOTSTRAP 5)

**templates/base.html**:
```html
<!DOCTYPE html>
<html lang="{{ current_lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_name }}</title>
    <link href="{{ url_for('static', filename='css/bootstrap.min.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/custom.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/schedule_grid.css') }}" rel="stylesheet">
</head>
<body>
    <!-- Top Toolbar -->
    {% include 'components/toolbar.html' %}
    
    <!-- Tabs -->
    <div class="container-fluid">
        <ul class="nav nav-tabs" id="mainTabs" role="tablist">
            <li class="nav-item">
                <a class="nav-tab" href="#teachers">{{ _('Teachers') }}</a>
            </li>
            <li class="nav-item">
                <a class="nav-tab" href="#groups">{{ _('Groups') }}</a>
            </li>
            <li class="nav-item">
                <a class="nav-tab" href="#subjects">{{ _('Subjects') }}</a>
            </li>
            <li class="nav-item disabled">
                <span class="nav-tab">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </li>
            <li class="nav-item">
                <a class="nav-tab" href="#day-view">{{ _('Day View') }}</a>
            </li>
            <li class="nav-item">
                <a class="nav-tab" href="#group-scheduler">{{ _('Group Scheduler') }}</a>
            </li>
            <li class="nav-item">
                <a class="nav-tab" href="#teacher-scheduler">{{ _('Teacher Scheduler') }}</a>
            </li>
            <li class="nav-item disabled">
                <span class="nav-tab">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
            </li>
            <li class="nav-item">
                <a class="nav-tab" href="#configuration">{{ _('General Configuration') }}</a>
            </li>
        </ul>
        
        <div class="tab-content">
            {% block content %}{% endblock %}
        </div>
    </div>
    
    <!-- Modals -->
    {% include 'components/confirmations.html' %}
    
    <script src="{{ url_for('static', filename='js/jquery.min.js') }}"></script>
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    <script src="{{ url_for('static', filename='js/api_client.js') }}"></script>
    <script src="{{ url_for('static', filename='js/i18n.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

**templates/teachers/list.html**:
```html
{% extends 'base.html' %}
{% block content %}
<div id="teachers" class="tab-pane">
    <div class="table-responsive">
        <table id="teachersTable" class="table table-striped table-hover">
            <thead>
                <tr>
                    <th>{{ _('Name') }}</th>
                    <th>{{ _('Subjects') }}</th>
                    <th class="text-end">{{ _('Assigned/Available') }}</th>
                </tr>
            </thead>
            <tbody>
                <!-- Populated by JavaScript -->
            </tbody>
        </table>
    </div>
    
    <div class="btn-group mt-3">
        <button class="btn btn-primary" onclick="editTeacher()">{{ _('Edit Selected') }}</button>
        <button class="btn btn-danger" onclick="deleteTeacher()">{{ _('Delete Selected') }}</button>
        <button class="btn btn-secondary" onclick="moveTeacher('up')">{{ _('Move Up ↑') }}</button>
        <button class="btn btn-secondary" onclick="moveTeacher('down')">{{ _('Move Down ↓') }}</button>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
$(document).ready(function() {
    loadTeachers();
});

function loadTeachers() {
    API.get('/api/teachers').then(teachers => {
        const tbody = $('#teachersTable tbody');
        tbody.empty();
        
        teachers.forEach(teacher => {
            const subjectsText = teacher.subjects.map(s => 
                `${s.name}:${s.hours}:${s.group}`
            ).join('; ');
            
            const assigned = teacher.subjects.reduce((sum, s) => sum + s.hours, 0);
            const available = Object.values(teacher.available_slots || {})
                .reduce((sum, arr) => sum + arr.length, 0);
            
            const row = $('<tr>')
                .data('teacher', teacher)
                .append($('<td>').text(teacher.name))
                .append($('<td>').text(subjectsText))
                .append($('<td>').addClass('text-end').text(`${assigned}/${available}`));
            
            tbody.append(row);
        });
        
        // Highlight selected row on click
        $('#teachersTable tbody tr').click(function() {
            $(this).addClass('table-active').siblings().removeClass('table-active');
        });
    });
}

function editTeacher() {
    const selected = $('#teachersTable tbody tr.table-active');
    if (selected.length === 0) {
        alert(_('Select a teacher to edit'));
        return;
    }
    
    const teacher = selected.data('teacher');
    showEditTeacherModal(teacher);
}
</script>
{% endblock %}
```

**templates/schedules/group_scheduler.html**:
```html
{% extends 'base.html' %}
{% block content %}
<div id="group-scheduler" class="tab-pane">
    <div class="control-panel mb-3">
        <label>{{ _('Select group:') }}</label>
        <select id="groupSelect" class="form-select" style="width:300px; display:inline-block;">
            <!-- Populated by JS -->
        </select>
        <button class="btn btn-success" onclick="autofillGroup()">{{ _('Autofill') }}</button>
        <button class="btn btn-warning" onclick="clearGroupSchedule()">{{ _('Clear') }}</button>
        <button class="btn btn-info" onclick="exportPDF()">{{ _('Print to PDF') }}</button>
    </div>
    
    <div id="scheduleGrid" class="schedule-grid">
        <!-- Generated by JavaScript -->
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/schedule_grid.js') }}"></script>
<script>
$(document).ready(function() {
    loadGroups();
    $('#groupSelect').change(loadGroupSchedule);
});

function loadGroups() {
    API.get('/api/groups').then(groups => {
        const select = $('#groupSelect');
        select.empty();
        groups.forEach(g => {
            select.append($('<option>').val(g.name).text(g.name));
        });
        loadGroupSchedule();
    });
}

function loadGroupSchedule() {
    const groupName = $('#groupSelect').val();
    if (!groupName) return;
    
    API.get(`/api/schedules/group/${groupName}`).then(schedule => {
        ScheduleGrid.render('#scheduleGrid', schedule, {
            mode: 'group',
            editable: true,
            onCellClick: (day, lesson) => showLessonModal(groupName, day, lesson)
        });
    });
}

function autofillGroup() {
    const groupName = $('#groupSelect').val();
    if (!groupName) return;
    
    if (!confirm(_('Rebuild the schedule? This will delete the current schedule and create a new one.'))) {
        return;
    }
    
    API.post('/api/schedules/autofill', { group: groupName }).then(result => {
        if (result.success) {
            alert(_('Schedule created successfully'));
            loadGroupSchedule();
        } else {
            alert(_('Errors occurred:') + '\n' + result.errors.join('\n'));
        }
    });
}
</script>
{% endblock %}
```

**static/js/schedule_grid.js**:
```javascript
const ScheduleGrid = {
    render(selector, schedule, options = {}) {
        const container = $(selector);
        container.empty();
        
        const config = options.config || window.APP_CONFIG;
        const weekdays = config.WEEKDAYS.split(',');
        const lessons = Array.from({length: config.lessons}, (_, i) => i + 1);
        
        // Create table
        const table = $('<table>').addClass('schedule-table');
        
        // Header row
        const headerRow = $('<tr>');
        headerRow.append($('<th>').text('Lesson'));
        weekdays.forEach(day => {
            headerRow.append($('<th>').text(day));
        });
        table.append(headerRow);
        
        // Data rows
        lessons.forEach(lesson => {
            const row = $('<tr>');
            row.append($('<td>').addClass('lesson-number').text(lesson));
            
            weekdays.forEach(day => {
                const cell = $('<td>').addClass('schedule-cell');
                const lessonData = schedule[day]?.[lesson];
                
                if (lessonData) {
                    cell.addClass('filled')
                        .css('background-color', lessonData.color_bg)
                        .css('color', lessonData.color_fg);
                    
                    const content = $('<div>').addClass('cell-content');
                    content.append($('<div>').addClass('subject').text(lessonData.subject));
                    content.append($('<div>').addClass('teacher').text(lessonData.teacher));
                    cell.append(content);
                }
                
                if (options.editable) {
                    cell.click(() => {
                        if (options.onCellClick) {
                            options.onCellClick(day, lesson, lessonData);
                        }
                    });
                }
                
                row.append(cell);
            });
            
            table.append(row);
        });
        
        container.append(table);
    }
};
```

---

### 5. MULTILINGUAL SUPPORT

**services/i18n.py**:
```python
# Copy ALL 670 lines from translations.py

GUI_TEXT = [
    "Add Teacher",           # 0 - English
    "Add Group",             # 1
    # ... (indices 0-200)
]

GUI_TEXT_HE = [
    "הוסף מורה",              # 0 - Hebrew
    "הוסף קבוצה",             # 1
    # ... (indices 0-200)
]

GUI_TEXT_RU = [
    "Добавить учителя",       # 0 - Russian
    "Добавить группу",        # 1
    # ... (indices 0-200)
]

def get_text(index, lang='English'):
    """Get translated text by index"""
    if lang == 'עברית':
        return GUI_TEXT_HE[index]
    elif lang == 'Русский':
        return GUI_TEXT_RU[index]
    else:
        return GUI_TEXT[index]

def get_all_texts(lang='English'):
    """Get all texts for client-side use"""
    if lang == 'עברית':
        return GUI_TEXT_HE
    elif lang == 'Русский':
        return GUI_TEXT_RU
    else:
        return GUI_TEXT
```

**app.py** (inject translations):
```python
from services.i18n import get_text, get_all_texts

@app.context_processor
def inject_i18n():
    lang = excel_service.get_config().get('GUI_LANGUAGE', 'English')
    return {
        '_': lambda idx: get_text(idx, lang),
        'texts': get_all_texts(lang),
        'current_lang': lang
    }

@app.route('/api/i18n/<lang>')
def get_translations(lang):
    """API endpoint for client-side translations"""
    return jsonify(get_all_texts(lang))
```

**static/js/i18n.js**:
```javascript
const I18N = {
    texts: {},
    
    async load(lang) {
        const response = await fetch(`/api/i18n/${lang}`);
        this.texts = await response.json();
    },
    
    t(index) {
        return this.texts[index] || `[Missing: ${index}]`;
    }
};

// Expose as global function
window._ = (index) => I18N.t(index);

// Load on page load
$(document).ready(() => {
    const lang = $('html').attr('lang');
    I18N.load(lang);
});
```

---

### 6. CONFIRMATION DIALOGS (DEFAULT: NO)

**static/js/confirmations.js**:
```javascript
const Confirmations = {
    show(title, message, callback) {
        const modal = $('#confirmationModal');
        modal.find('.modal-title').text(title);
        modal.find('.modal-body').text(message);
        
        // Default focus on NO button
        modal.find('.btn-secondary').focus();
        
        modal.find('.btn-primary').off('click').on('click', () => {
            modal.modal('hide');
            callback(true);
        });
        
        modal.find('.btn-secondary').off('click').on('click', () => {
            modal.modal('hide');
            callback(false);
        });
        
        modal.modal('show');
    },
    
    saveConfig(callback) {
        this.show(
            _('Confirm'),
            _('Are you sure you want to save the configuration? This will apply the changes.'),
            callback
        );
    },
    
    clearSchedules(callback) {
        this.show(
            _('Confirm'),
            _('Delete all schedules? This will remove all generated schedules but keep Teachers, Groups, and Subjects.'),
            callback
        );
    },
    
    // ... similar for all confirmation types
};
```

---

### 7. PDF EXPORT (WeasyPrint)

**services/pdf_service.py**:
```python
from weasyprint import HTML, CSS
from jinja2 import Template
import os

class PDFService:
    def export_schedule(self, schedule, config, output_path):
        """Export schedule to PDF using WeasyPrint"""
        
        # Render HTML template
        template = Template('''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @page { size: A4 landscape; margin: 1cm; }
                body { font-family: Arial, sans-serif; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #000; padding: 8px; text-align: center; }
                th { background-color: #ccc; }
                .subject { font-weight: bold; }
                .teacher { font-size: 0.9em; color: #666; }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <table>
                <thead>
                    <tr>
                        <th>Lesson</th>
                        {% for day in weekdays %}
                        <th>{{ day }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for lesson in lessons %}
                    <tr>
                        <td>{{ lesson }}</td>
                        {% for day in weekdays %}
                        <td style="background-color: {{ schedule[day][lesson].color_bg if schedule[day][lesson] else '#fff' }}">
                            {% if schedule[day][lesson] %}
                            <div class="subject">{{ schedule[day][lesson].subject }}</div>
                            <div class="teacher">{{ schedule[day][lesson].teacher }}</div>
                            {% endif %}
                        </td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
        ''')
        
        html_content = template.render(
            title=config.get('app_name', 'Schedule'),
            weekdays=config['WEEKDAYS'].split(','),
            lessons=range(1, int(config['lessons']) + 1),
            schedule=schedule
        )
        
        # Convert to PDF
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path
```

---

### 8. DEPLOYMENT

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    restart: unless-stopped
```

**requirements.txt**:
```
Flask==2.3.0
flask-cors==4.0.0
openpyxl==3.1.0
WeasyPrint==59.0
gunicorn==21.0.0
python-dotenv==1.0.0
```

**README.md**:
```markdown
# School Scheduler Web

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run development server:
```bash
python app.py
```

3. Open browser: http://localhost:5000

## Docker Deployment

```bash
docker-compose up -d
```

## Render.com Deployment

1. Push to GitHub
2. Connect Render to repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
```

---

## TESTING CHECKLIST

Generate unit tests for:

✅ **Autofill Algorithm**:
- Test with 5 teachers, 3 groups, 10 subjects
- Test conflict detection (no double-booking)
- Test constraints (max_sequence_lessons, max_per_day)
- Test Teachers Weekly Hours priority over Availability

✅ **Excel I/O**:
- Test import/export roundtrip (data integrity)
- Test multiple shifts parsing (Monday:08:00-12:00; Monday:13:00-17:00)
- Test Teachers Weekly Hours → available_slots conversion

✅ **Multilingual**:
- Test language switching (English, Hebrew, Russian)
- Test all 200+ translated strings load correctly
- Test RTL layout for Hebrew

✅ **API Endpoints**:
- Test CRUD for teachers, groups, subjects
- Test autofill API response
- Test error handling (404, 400)

✅ **Schedule Grid Rendering**:
- Test empty grid display
- Test filled grid with colors
- Test cell click interactions

---

## OUTPUT

Generate:

1. **Complete codebase** in the structure above
2. **All 670 lines** of translations from translations.py
3. **Autofill algorithm** ported from app_core.py L341-540
4. **Excel import/export** ported from buttons_functions.py L321-814
5. **Bootstrap 5 UI** matching Tkinter layout pixel-perfect
6. **Unit tests** for all critical functions
7. **Docker setup** for easy deployment
8. **README** with detailed setup instructions

**Priority**: Teachers Weekly Hours > Availability (CRITICAL!)

**Start generating now.**
