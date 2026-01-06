from flask import Flask
import sys
import os

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from routes import admin_routes
from services.excel_service import ExcelService

app = Flask(__name__)

if __name__ == '__main__':
    # create excel service using default data file
    excel = ExcelService('data/schedule_test_export.xlsx')
    admin_routes.init_routes(excel_svc=excel)

    # run export silently; return value can be inspected programmatically
    with app.test_request_context():
        resp = admin_routes.export_excel()
        try:
            data = resp.get_json()
        except Exception:
            data = None
        # do not print in non-debug mode; just return
        # if run as script, keep silent
        _ = data
