from services.excel_service import ExcelService
from services.import_service import ImportService
import os

base = os.path.dirname(os.path.dirname(__file__))
example = os.path.join(base, 'ExcelExamples', 'export_Good.xlsx')
if not os.path.exists(example):
    print('Example file not found:', example)
    raise SystemExit(1)

# Use a fresh excel data file for import results
data_dir = os.path.join(base, 'data')
os.makedirs(data_dir, exist_ok=True)
user_xlsx = os.path.join(data_dir, 'user_import_test.xlsx')
# remove if exists
try:
    if os.path.exists(user_xlsx):
        os.remove(user_xlsx)
except Exception:
    pass

excel = ExcelService(file_path=user_xlsx)
importer = ImportService(excel)
res = importer.import_from_file(example)
print('Import result:', res)
print('Counts after import:')
print('Teachers:', len(excel.get_teachers()))
print('Groups:', len(excel.get_groups()))
print('Subjects:', len(excel.get_subjects()))
# Show first 5 teachers
for t in excel.get_teachers()[:5]:
    print('T:', t.get('name'), 'subjects:', t.get('subjects'))
