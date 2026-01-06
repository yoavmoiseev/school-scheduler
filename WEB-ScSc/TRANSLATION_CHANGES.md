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
