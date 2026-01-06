"""Generate services/i18n_he.json and services/i18n_ru.json for translators.

Usage:
    python scripts/generate_i18n_jsons.py

This will read `services/i18n.py`, collect the English master list and
current Hebrew/Russian arrays (if present) and write two JSON files
with the same length as the English master. Existing translations are kept;
missing entries are written as empty strings for translators to fill.
"""
import runpy
import json
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
I18N_PATH = os.path.join(ROOT, 'services', 'i18n.py')
HE_OUT = os.path.join(ROOT, 'services', 'i18n_he.json')
RU_OUT = os.path.join(ROOT, 'services', 'i18n_ru.json')

print('Loading', I18N_PATH)
ctx = runpy.run_path(I18N_PATH)
GUI_TEXT = ctx.get('GUI_TEXT', [])
GUI_TEXT_HE = ctx.get('GUI_TEXT_HE', [])
GUI_TEXT_RU = ctx.get('GUI_TEXT_RU', [])

n = len(GUI_TEXT)
he_out = []
ru_out = []
for i in range(n):
    he_val = GUI_TEXT_HE[i] if i < len(GUI_TEXT_HE) and GUI_TEXT_HE[i] else ''
    ru_val = GUI_TEXT_RU[i] if i < len(GUI_TEXT_RU) and GUI_TEXT_RU[i] else ''
    he_out.append(he_val)
    ru_out.append(ru_val)

with open(HE_OUT, 'w', encoding='utf-8') as f:
    json.dump(he_out, f, ensure_ascii=False, indent=2)
with open(RU_OUT, 'w', encoding='utf-8') as f:
    json.dump(ru_out, f, ensure_ascii=False, indent=2)

print('Wrote:', HE_OUT, RU_OUT)
print('Entries:', n)
