"""Apply translated JSON arrays into services/i18n.py inlined `GUI_TEXT_HE` and `GUI_TEXT_RU`.

Usage:
    python scripts/apply_i18n_translations.py

Behavior:
- Reads services/i18n.py to determine English master list length.
- Loads services/i18n_he.json and services/i18n_ru.json (must be arrays).
- Validates that both translation arrays have the exact length as the English master.
- Creates a timestamped backup of services/i18n.py.
- Replaces the final occurrences of `GUI_TEXT_HE = [...]` and `GUI_TEXT_RU = [...]`
  with the provided JSON arrays serialized as Python list literals.
- Attempts a quick import syntax check after writing.

Safety: The script will abort without modifying the file if lengths mismatch or
if JSON files are missing/wrong. Always review the backup placed alongside
`services/i18n.py` before committing.
"""
import runpy, json, os, sys, shutil, time, re

ROOT = os.path.dirname(os.path.dirname(__file__))
I18N_PY = os.path.join(ROOT, 'services', 'i18n.py')
HE_JSON = os.path.join(ROOT, 'services', 'i18n_he.json')
RU_JSON = os.path.join(ROOT, 'services', 'i18n_ru.json')

if not os.path.exists(I18N_PY):
    print('ERROR: services/i18n.py not found')
    sys.exit(2)

ctx = runpy.run_path(I18N_PY)
GUI_TEXT = ctx.get('GUI_TEXT', [])
N = len(GUI_TEXT)
print('English master length:', N)

# Load translations
if not os.path.exists(HE_JSON) or not os.path.exists(RU_JSON):
    print('ERROR: Translation JSON files not found. Expected:', HE_JSON, RU_JSON)
    sys.exit(3)

with open(HE_JSON, 'r', encoding='utf-8') as f:
    he = json.load(f)
with open(RU_JSON, 'r', encoding='utf-8') as f:
    ru = json.load(f)

if not isinstance(he, list) or not isinstance(ru, list):
    print('ERROR: JSON files must contain arrays of strings')
    sys.exit(4)

if len(he) != N or len(ru) != N:
    print('ERROR: Length mismatch: English=', N, 'HE=', len(he), 'RU=', len(ru))
    print('Fill the JSON arrays so they exactly match English indices.')
    sys.exit(5)

# Backup
bak = I18N_PY + '.bak.' + time.strftime('%Y%m%d_%H%M%S')
shutil.copy2(I18N_PY, bak)
print('Backup created:', bak)

# Read source
with open(I18N_PY, 'r', encoding='utf-8') as f:
    src = f.read()

# Helper: find last occurrence of assignment and replace the matching list
def find_and_replace_last_list(text, varname, new_list_py):
    # find all occurrences of 'varname' followed by '=' and '['
    pattern = re.compile(rf"{re.escape(varname)}\s*=\s*\[", re.M)
    matches = list(pattern.finditer(text))
    if not matches:
        raise RuntimeError(f'Variable {varname} assignment not found')
    m = matches[-1]
    start = m.start()
    # find position of the first '[' from the match
    bracket_pos = text.find('[', m.end()-1)
    if bracket_pos == -1:
        raise RuntimeError('Opening bracket not found')
    # Find matching closing bracket while ignoring brackets inside strings
    i = bracket_pos
    depth = 0
    in_sq = False
    in_dq = False
    esc = False
    while i < len(text):
        ch = text[i]
        if esc:
            esc = False
        elif ch == '\\':
            esc = True
        elif ch == "'" and not in_dq:
            in_sq = not in_sq
        elif ch == '"' and not in_sq:
            in_dq = not in_dq
        elif not in_sq and not in_dq:
            if ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    end = i
                    break
        i += 1
    else:
        raise RuntimeError('Matching closing bracket not found')
    # Replace from start (varname...) up to end (inclusive) with new_list_py
    new_text = text[:start] + f"{varname} = {new_list_py}\n\n" + text[end+1:]
    return new_text

# Serialize Python list literal using json.dumps (valid Python syntax for simple lists)
new_he_py = json.dumps(he, ensure_ascii=False, indent=4)
new_ru_py = json.dumps(ru, ensure_ascii=False, indent=4)

try:
    src2 = find_and_replace_last_list(src, 'GUI_TEXT_HE', new_he_py)
    src3 = find_and_replace_last_list(src2, 'GUI_TEXT_RU', new_ru_py)
except Exception as e:
    print('ERROR while replacing lists:', e)
    print('Restoring from backup')
    shutil.copy2(bak, I18N_PY)
    sys.exit(6)

# Write new file
with open(I18N_PY, 'w', encoding='utf-8') as f:
    f.write(src3)
print('Wrote updated', I18N_PY)

# Quick syntax check
try:
    runpy.run_path(I18N_PY)
    print('Syntax check OK')
except Exception as e:
    print('Syntax check failed:', e)
    print('Restoring backup')
    shutil.copy2(bak, I18N_PY)
    sys.exit(7)

print('Done. Review the backup file before committing changes.')
