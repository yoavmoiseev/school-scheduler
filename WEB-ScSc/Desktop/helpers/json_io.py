import os
import json

def _load_json(file_path, key=None):
    """Load JSON data from file. If key provided, return list under that key or []"""
    if not os.path.exists(file_path):
        return [] if key else {}
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if key:
        if isinstance(data, dict) and key in data:
            return data[key]
        if isinstance(data, list):
            return data
        return []
    return data

def write_append_json(file_path, key, item):
    """Append an item to a list under 'key' in a JSON file. Create file/key when missing."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data = None
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = None
    if data is None:
        data = {key: [item]}
    elif isinstance(data, dict) and key in data and isinstance(data[key], list):
        data[key].append(item)
    elif isinstance(data, list):
        data.append(item)
    else:
        data = {key: [item]}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_save_json(file_path, key, items):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    data = {key: items}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_save_dict(file_path, data_dict):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=2)
