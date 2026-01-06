print("Starting imports...")

try:
    from flask import Flask
    print("Flask imported OK")
    
    from services.excel_service import ExcelService
    print("ExcelService imported OK")
    
    from services.autofill_service import AutofillService
    print("AutofillService imported OK")
    
    from services.conflict_checker import ConflictChecker
    print("ConflictChecker imported OK")
    
    from services.import_service import ImportService
    print("ImportService imported OK")
    
    print("\nAll imports successful!")
    
    # Try creating ExcelService
    print("\nTrying to create ExcelService...")
    excel = ExcelService('data/schedule.xlsx')
    print("ExcelService created OK")
    
    # Try getting data
    print("\nTrying to get config...")
    config = excel.get_config()
    print(f"Config loaded: {config}")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete!")
