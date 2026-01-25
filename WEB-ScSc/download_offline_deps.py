"""
Script to download all external dependencies for offline use
Compatible with Windows 7, 8, 10, 11
"""
import os
import urllib.request
import sys

# Define what to download
DEPENDENCIES = {
    # Bootstrap CSS
    'static/vendor/bootstrap/bootstrap.min.css': 
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'static/vendor/bootstrap/bootstrap.min.css.map': 
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css.map',
    
    # Bootstrap JS
    'static/vendor/bootstrap/bootstrap.bundle.min.js': 
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'static/vendor/bootstrap/bootstrap.bundle.min.js.map': 
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js.map',
    
    # jQuery
    'static/vendor/jquery/jquery-3.6.0.min.js': 
        'https://code.jquery.com/jquery-3.6.0.min.js',
}

def download_file(url, dest_path):
    """Download a file from URL to destination path"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        print(f"Downloading {url}...")
        print(f"  -> {dest_path}")
        
        # Download with progress
        urllib.request.urlretrieve(url, dest_path)
        
        print(f"  ✓ Success")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False

def main():
    """Download all dependencies"""
    print("=" * 60)
    print("Downloading offline dependencies for School Scheduler")
    print("=" * 60)
    print()
    
    success_count = 0
    fail_count = 0
    
    for dest, url in DEPENDENCIES.items():
        if download_file(url, dest):
            success_count += 1
        else:
            fail_count += 1
        print()
    
    print("=" * 60)
    print(f"Download complete: {success_count} succeeded, {fail_count} failed")
    print("=" * 60)
    
    if fail_count > 0:
        print("\n⚠ Warning: Some files failed to download.")
        print("The application may not work properly offline.")
        return 1
    else:
        print("\n✓ All dependencies downloaded successfully!")
        print("The application is ready for offline use.")
        return 0

if __name__ == '__main__':
    sys.exit(main())
