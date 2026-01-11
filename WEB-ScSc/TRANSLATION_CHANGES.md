# Translation changes log

All translation edits performed by the assistant are recorded here.

## 2026-01-05 — Initial bulk overrides added by assistant
- Keys added to `services/i18n_he_new.json` and `services/i18n_ru_new.json`:
  - "Delete all data files (teachers/groups/subjects/schedules)?"
  - "Are you sure you want to logout?"
  - "Set priorities for rebuild. Use Up/Down to change order. Press Run when ready."
  - "Run"
  - "Days Priority"
  - "Teachers Priority"
  - "Subjects Priority"
  - "Groups Priority"
  - "⚠️ Priority Order:<br>Teacher's Weekly Hours (PRIMARY) - If provided, Time Slots and Lessons are calculated from this<br>Time Slots (SECONDARY) - Used only if Weekly Hours is empty. Converted to lesson numbers<br>Lessons (TERTIARY) - Used only if both above are empty"

Files modified:
- `services/i18n_he_new.json` (overrides added)
- `services/i18n_ru_new.json` (overrides added)
- `services/i18n.py` (support for new override files / client overrides)
- `static/js/i18n.js` (client now applies overrides)
- `scripts/export_i18n_new.py` (export utility added)
- `TRANSLATION_PROCESS.RMD` (process documentation added/updated)

## 2026-01-06 — Russian override for "School Scheduler"
- Added partial override for Russian in `services/i18n_ru_new.json`:
  - "School Scheduler": "Редактор расписания школы"

Files modified:
- `services/i18n_ru_new.json` (added override)

Notes:
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes. This fixes the Russian text displayed on the login page title.

## 2026-01-06 — Russian overrides for login texts
- Added partial overrides for Russian in `services/i18n_ru_new.json`:
  - "Login to your account": "Войдите в свою учётную запись"
  - "Don't have an account?": "Ещё нет аккаунта?"

Files modified:
- `services/i18n_ru_new.json` (added overrides)

Notes:
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes. This updates the login card text and the signup prompt in Russian.

## 2026-01-06 — Hebrew override for login prompt
- Added partial override for Hebrew in `services/i18n_he_new.json`:
  - "Don't have an account?": "אין חשבון?"

Files modified:
- `services/i18n_he_new.json` (added override)

Notes:
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes. This updates the signup prompt in Hebrew.

## 2026-01-06 — Russian override for 'Sign Up'
- Added partial override for Russian in `services/i18n_ru_new.json`:
  - "Sign Up": "Зарегистрироваться"

Files modified:
- `services/i18n_ru_new.json` (added override)

Notes:
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes. This updates the 'Sign Up' button/text in Russian.

Notes:
- After these edits, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes.
- All future edits must follow the documented process in `TRANSLATION_PROCESS.RMD`.
## 2026-01-11 — Russian overrides for signup form fields
- Added partial overrides for Russian in `services/i18n_ru_new.json`:
  - "First Name": "Имя"
  - "Last Name": "Фамилия"
  - "Email (optional)": "Email (необязательно)"
  - "Username": "Имя пользователя"
  - "Password": "Пароль"
  - "Confirm Password": "Подтвердите пароль"
  - "Create your account": "Создайте аккаунт"
  - "Already have an account?": "Уже есть аккаунт?"
  - "Login": "Войти"
  - "Username must be at least 3 characters and contain only letters, numbers, and underscores": "Имя пользователя должно содержать не менее 3 символов и может включать только буквы, цифры и символ подчёркивания"
  - "Password must be at least 6 characters": "Пароль должен содержать не менее 6 символов"

Files modified:
- `services/i18n_ru_new.json` (added overrides)

Notes:
- This fixes the signup form where Russian translations were shifted/misaligned, causing fields to show wrong labels (e.g., "Регистрация" instead of "Подтвердите пароль")
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes
- All form fields and tooltips in the signup page should now display correct Russian translations

## 2026-01-11 — Hebrew override for "Already have an account?"
- Added partial override for Hebrew in `services/i18n_he_new.json`:
  - "Already have an account?": "כבר יש לך חשבון?"

Files modified:
- `services/i18n_he_new.json` (added override)

Notes:
- This fixes the missing Hebrew translation in the signup form
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes

## 2026-01-11 — Russian overrides for menu buttons
- Added partial overrides for Russian in `services/i18n_ru_new.json`:
  - "Save to Favorites": "Сохранить в избранное"
  - "Load from Favorites": "Загрузить из избранного"
  - "Rebuild All": "Перестроить всё"
  - "Clear All Schedulers": "Очистить все расписания"
  - "Clear All Data": "Очистить все данные"
  - "Logout": "Выйти"

Files modified:
- `services/i18n_ru_new.json` (added overrides)

Notes:
- This ensures correct Russian translations for main menu buttons and actions
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes

## 2026-01-11 — Russian overrides for 45+ UI elements (comprehensive fix)
- Added partial overrides for Russian in `services/i18n_ru_new.json`:
  - Authentication: "Passwords do not match", "Account created successfully!", "Signup failed", "Login failed", "An error occurred. Please try again.", "Logout failed"
  - Modal dialogs: "Confirm", "Cancel", "Close", "Delete", "OK", "Save"
  - Favorites: "Saved to Favorites", "Enter favorite name:", "Rename", "Enter new name:", "Delete this favorite?", "No favorites saved", "Favorites"
  - Rebuild/Export: "Rebuild All (Autofill)", "Before rebuilding...", "I already exported", "Export now", "Import from Excel", "Export to Excel", "Running...", "Success", "Failed"
  - Teachers: "Add Teacher", "Edit Teacher", "Select a teacher to edit/delete/move", "Teacher name is required"
  - Groups/Subjects: "Add Group", "Edit Group", "Add Subject", "Edit Subject", "Select a group/subject to edit"
  - Time slots: "Click to set time", "Click to edit", "Delete slot", "Add Slot", "Time Range (click to edit)"

Files modified:
- `services/i18n_ru_new.json` (added 45+ overrides)

Notes:
- This is a comprehensive fix for Russian translations across the entire interface
- Fixes error messages, modal dialogs, buttons, and interactive elements
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes
- All major UI elements should now display correct, natural Russian text

## 2026-01-11 — Russian override for clear all data confirmation
- Added partial override for Russian in `services/i18n_ru_new.json`:
  - "All existing data will be erased. An Export to Excel will run first. Continue?": "Все данные будут удалены. Сначала произойдёт экспорт в Excel. Продолжить?"

Files modified:
- `services/i18n_ru_new.json` (added override)

Notes:
- This fixes the confirmation dialog for clearing all data, which was previously untranslated
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes

## 2026-01-11 — Russian override for "Day Scheduler"
- Added partial override for Russian in `services/i18n_ru_new.json`:
  - "Day Scheduler": "Расписание дня"

Files modified:
- `services/i18n_ru_new.json` (added override)

Notes:
- This fixes the tab name which was incorrectly translated as "Выберите день недели" (Select weekday)
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes

## 2026-01-11 — Hebrew overrides for scheduler terms (מתזמן → מערכת)
- Added partial overrides for Hebrew in `services/i18n_he_new.json`:
  - "School Scheduler": "בונה מערכת לבית ספר" (instead of "מתזמן בית ספר")
  - "Day Scheduler": "מערכת ליום" (instead of "מתזמן יום")
  - "Teacher Scheduler": "מערכת למורה" (instead of "מתזמן מורים")
  - "Group Scheduler": "מערכת לקבוצה" (instead of "מתזמן קבוצות")

Files modified:
- `services/i18n_he_new.json` (added overrides)

Notes:
- This replaces the word "מתזמן" with more appropriate "מערכת" terminology
- After this change, restart the server and hard-refresh the browser (Ctrl+F5) to pick up client-side changes

## 2026-01-11 — Configuration improvements: max_autofill_retries default & login language sync
- Changed default value of `max_autofill_retries` from 15 to 2 for new users
- Added automatic synchronization of login language selection to user's GUI_LANGUAGE config

Files modified:
- `config.py` (changed MAX_AUTOFILL_RETRIES default from 15 to 2)
- `services/excel_service.py` (changed default max_autofill_retries in _create_default from 15 to 2)
- `routes/auth_routes.py` (added language parameter to login endpoint and save to session)
- `templates/login.html` (send selected language with login request)
- `app.py` (use login language to set GUI_LANGUAGE in user's config)

Notes:
- New users will now have max_autofill_retries = 2 by default (instead of 15)
- When logging in, the language selected in the dropdown will automatically be saved to the user's GUI_LANGUAGE setting
- This ensures the General tab's "GUI Language" field matches the login language selection
- After this change, restart the server to apply the changes

## 2026-01-11 — Export to Excel: Add "Empty" label for empty teacher slots
- Modified teacher schedule export to display "Empty" only in available time slots where no lesson is assigned

Files modified:
- `routes/admin_routes.py` (added "Empty" label only for available but unassigned slots in Teacher_ sheets)

Notes:
- When exporting to Excel, only time slots within a teacher's Available Hours that have no lesson assigned will show "Empty"
- Time slots outside the teacher's availability remain blank
- This makes it clear which available slots are unassigned vs slots where the teacher is not available
- After this change, restart the server to apply the changes

## 2026-01-11 — UI Improvement: Move Save button to top of Configuration tab
- Moved the Save button from bottom to top of the Configuration form for better UX

Files modified:
- `templates/index.html` (moved Save button to line ~145, at top of Configuration form)

Notes:
- The Save button is now immediately visible without scrolling
- This improves usability for users who make configuration changes
- After this change, restart the server and hard-refresh the browser (Ctrl+F5)

## 2026-01-11 — AutoFill preserves manually selected lessons (Rebuild All unaffected)
- Modified AutoFill function to preserve manually selected lessons and only fill empty slots
- Rebuild All continues to work as before (full rebuild from scratch)

Files modified:
- `services/autofill_service.py` (added preserve_existing parameter to autofill_group function)
- `routes/admin_routes.py` (Rebuild All calls autofill with preserve_existing=False)

Key changes:
- `autofill_group()` now has a `preserve_existing` parameter (default=True)
- When `preserve_existing=True` (AutoFill button in Groups Scheduler):
  - Loads existing group schedule from Excel
  - Preserves all existing lessons
  - Only fills empty time slots
  - Marks teachers of preserved lessons as busy to avoid conflicts
- When `preserve_existing=False` (Rebuild All):
  - Starts with empty schedule (old behavior)
  - Completely rebuilds schedule from scratch
- `/api/schedules/autofill` endpoint uses default `preserve_existing=True`
- Rebuild All explicitly passes `preserve_existing=False`

Behavior:
- **AutoFill button**: Users can manually place some lessons, then click AutoFill to complete the schedule
- **Rebuild All button**: Clears everything and rebuilds all group schedules from scratch
- **No changes** to Rebuild All logic - it works exactly as before

Notes:
- After this change, restart the server to apply the changes
- Test workflow: 1) Manually assign some lessons to a group, 2) Click AutoFill, 3) Verify manual lessons are preserved and empty slots are filled
- Test Rebuild All: Verify it still clears and rebuilds everything from scratch
