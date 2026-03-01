# Changelog

---

## [2026-03-01] — Session Summary

### 🌐 Translations (i18n)

**Files:** `services/i18n_he_new.json`, `services/i18n_ru_new.json`

- Added Hebrew and Russian translations for Import modal strings:
  - `"Import from Excel"`, `"Select Excel file from ExcelExamples folder:"`
  - `"Or choose a local file:"`, `"If you select a local file, it will be uploaded and imported."`
  - `"Loading..."`, `"Search..."`, `"Original order"`
- Added `"United groups"` translation (HE: `קבוצות מאוחדות`, RU: `Объединённые группы`)
- Note: `"Choose file" / "No file chosen"` — native browser text, cannot be translated via i18n

---

### 🔁 Rebuild All — Results UI

**File:** `static/js/form_handlers.js`

- **Virtual groups moved to bottom** — regular groups shown first; united/virtual groups collapsed at the bottom in a Bootstrap collapsible block (`▼ United groups (N)`)
- **Teacher combobox fixed** — now collects unique teachers from ALL incomplete placements (not just the first subject). If multiple teachers — shows a `<select>` dropdown; if one — shows a direct link button
- **Auto-close new tab after Edit Teacher popup** — when a tab is opened via "Open Teacher" deep-link, it now automatically closes (`window.close()`) when the Edit Teacher modal is dismissed (`hidden.bs.modal`, `{ once: true }`)
- **Renamed "Virtual groups" → "United groups"** in the collapse button label to match terminology used elsewhere in the app

---

### 📊 Rebuild All — Subject Priority

**Files:** `routes/admin_routes.py`, `services/autofill_service.py`

- **`priorities_data()` endpoint** now returns subjects pre-sorted by complexity score:
  - **Tier 0** — subjects belonging to United Groups (must be placed first — shared across sub-groups)
  - **Tier 1** — multi-teacher subjects (subgroups feature — all teachers must be free simultaneously)
  - **Tier 2** — regular subjects with a specific group, sorted by `hours_per_week` desc + teacher scarcity
  - **Tier 3** — orphan subjects (`group=''`) — placed last
  - Fixed bug: orphan subjects previously floated to the top due to division-by-zero in old formula
- **User can override** the auto-sorted order in the Rebuild All priorities UI before running
- **`autofill_group()`** now accepts `subject_order=None` parameter:
  - If provided (from Rebuild All) — sorts `group_subjects` by the given order
  - If not provided (manual single-group autofill) — fallback: multi-teacher subjects first, then by `hours_per_week` desc
- **`rebuild_all` endpoint** extracts `priorities.subjects` and passes it to all `autofill_group()` calls (both united and regular phases)

---

### 🔍 Search & Sort — Teachers / Groups / Subjects Tabs

**Files:** `templates/index.html`, `static/js/form_handlers.js`

- Added search input + sort buttons above each of the three main tables:
  - 🔍 Live search — filters rows by name prefix as user types (`startsWith`)
  - `⇑ A–Z` — lexicographic ascending sort
  - `⇓ Z–A` — lexicographic descending sort
  - `Original order` — resets to server-returned order
- Refactored `loadTeachers()`, `loadSubjects()`, `loadGroups()` to cache data in `window._teachersData`, `window._subjectsData`, `window._groupsData` and delegate rendering to `renderTeachers()`, `renderSubjects()`, `renderGroups()`

---

### 🔍 Search — Edit Teacher Modal (Available Subjects)

**Files:** `templates/components/confirmations.html`, `static/js/form_handlers.js`

- Added `<input id="availableSubjectsSearch">` above the Available Subjects `<select>`
- Filters the subject list by name prefix as user types
- All options cached in `window._availableSubjectsAll`; search calls `filterAvailableSubjects(q)`
- Search box is cleared automatically when the modal opens

---

### Files Changed This Session

| File | Changes |
|------|---------|
| `services/i18n_he_new.json` | +7 translation keys |
| `services/i18n_ru_new.json` | +7 translation keys |
| `static/js/form_handlers.js` | Rebuild results UI, teacher combobox, auto-close tab, search/sort for all 3 tabs + modal |
| `templates/index.html` | Search+sort toolbar for Teachers, Groups, Subjects tabs |
| `templates/components/confirmations.html` | Search input above Available Subjects list |
| `routes/admin_routes.py` | `priorities_data()` complexity sort, `rebuild_all` passes `subject_order` |
| `services/autofill_service.py` | `autofill_group()` `subject_order` param + smart fallback sort |
