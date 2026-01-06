"""Export current in-memory i18n arrays into new JSON templates.

Creates `services/i18n_text_new.json`, `services/i18n_he_new.json`,
and `services/i18n_ru_new.json` as full-list JSON files so they can be
edited and later picked up by `services/i18n.py`.
"""
import json
import os
import importlib.util
import sys


def _load_i18n_module(path):
    spec = importlib.util.spec_from_file_location('i18n_module', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    base = os.path.join(os.path.dirname(__file__), '..', 'services')
    i18n_path = os.path.join(base, 'i18n.py')
    mod = _load_i18n_module(i18n_path)

    out_text = os.path.join(base, 'i18n_text_new.json')
    out_he = os.path.join(base, 'i18n_he_new.json')
    out_ru = os.path.join(base, 'i18n_ru_new.json')

    with open(out_text, 'w', encoding='utf-8') as f:
        json.dump(mod.GUI_TEXT, f, ensure_ascii=False, indent=2)
    with open(out_he, 'w', encoding='utf-8') as f:
        json.dump(mod.GUI_TEXT_HE, f, ensure_ascii=False, indent=2)
    with open(out_ru, 'w', encoding='utf-8') as f:
        json.dump(mod.GUI_TEXT_RU, f, ensure_ascii=False, indent=2)

    print('Exported i18n_text_new.json, i18n_he_new.json, i18n_ru_new.json to', base)


if __name__ == '__main__':
    main()
