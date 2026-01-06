from flask import Flask, render_template, jsonify, send_file, session, redirect, url_for, g, request
from flask_cors import CORS
from config import Config
from datetime import timedelta
import os

# Import services
from services.excel_service import ExcelService
from services.autofill_service import AutofillService
from services.conflict_checker import ConflictChecker
from services.color_service import ColorService
from services.auth_service import AuthService
from services.import_service import ImportService
from services.i18n import get_text, get_all_texts, is_rtl
import source_consts

# Import routes
from routes.teachers import teachers_bp
from routes.groups import groups_bp
from routes.subjects import subjects_bp
from routes.schedules import schedules_bp
from routes.config_routes import config_bp
from routes.auth_routes import auth_bp
from routes.import_routes import import_bp
from routes.admin_routes import admin_bp
from routes.favorites_routes import favorites_bp

# Import route initializers
from routes import teachers, groups, subjects, schedules, config_routes, auth_routes, import_routes
from routes import admin_routes

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
CORS(app)

# Initialize auth service
auth_service = AuthService()

# Initialize auth routes
auth_routes.init_routes(auth_service)

# Register auth blueprint
app.register_blueprint(auth_bp)


# Get user-specific Excel service
def get_user_excel_service():
    """Get ExcelService for current logged-in user"""
    if 'excel_service' not in g:
        if 'username' in session:
            g.excel_service = ExcelService(username=session['username'])
        else:
            # Default service for non-authenticated access
            g.excel_service = ExcelService(app.config['EXCEL_FILE'])
    return g.excel_service


# Initialize conflict checker and color service (shared across users)
conflict_checker = ConflictChecker()
color_service = ColorService()


# Before request - setup user services
@app.before_request
def before_request():
    """Setup user-specific services before each request"""
    # Skip auth for static files and auth routes
    if any([
        '/static/' in str(request.path),
        '/api/auth/' in str(request.path),
        '/api/i18n/' in str(request.path),
        '/login' in str(request.path),
        '/signup' in str(request.path)
    ]):
        return
    
    # Redirect to login if not authenticated
    if 'user_id' not in session:
        if request.path != '/login' and not request.path.startswith('/api/auth/'):
            return redirect(url_for('auth.login_page'))
    
    # Setup user services
    excel_service = get_user_excel_service()
    autofill_service = AutofillService(excel_service, conflict_checker, color_service)
    import_service = ImportService(excel_service)
    
    # Re-initialize routes with user-specific services
    teachers.init_routes(excel_service)
    groups.init_routes(excel_service)
    subjects.init_routes(excel_service)
    schedules.init_routes(excel_service, autofill_service)
    config_routes.init_routes(excel_service)
    import_routes.init_routes(import_service)
    # admin routes
    admin_routes.init_routes(excel_service, autofill_service)


# Register blueprints
app.register_blueprint(teachers_bp)
app.register_blueprint(groups_bp)
app.register_blueprint(subjects_bp)
app.register_blueprint(schedules_bp)
app.register_blueprint(config_bp)
app.register_blueprint(import_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(favorites_bp)


# Context processor for i18n
@app.context_processor
def inject_i18n():
    # Language selection priority:
    # 1) URL query param `?lang=` if present and valid
    # 2) logged-in user's GUI_LANGUAGE (from their config)
    # 3) Accept-Language header best match
    # 4) global GUI_LANGUAGE in `source_consts.py`
    # 5) Config.DEFAULT_LANGUAGE fallback

    lang = None
    # 1) query param
    lang_param = request.args.get('lang')
    available_langs = getattr(source_consts, 'LANGUAGES_LIST', app.config.get('LANGUAGES_LIST', ['English']))
    if lang_param and lang_param in available_langs:
        lang = lang_param

    # 2) logged-in user's preference
    app_name = app.config.get('APP_NAME', 'School Scheduler')
    if not lang and 'username' in session:
        try:
            excel_service = get_user_excel_service()
            config = excel_service.get_config()
            lang = config.get('GUI_LANGUAGE') or None
            app_name = config.get('app_name', app_name)
        except Exception:
            # If user-specific service fails, ignore and continue to other fallbacks
            lang = lang

    # 3) Accept-Language header (map language codes to display names)
    if not lang:
        try:
            # Map common language codes to our display names
            lang_codes_map = {
                'en': 'English',
                'he': 'Hebrew',
                'iw': 'Hebrew',
                'ru': 'Russian'
            }
            # Ask Werkzeug to best-match against short codes
            best_code = request.accept_languages.best_match(list(lang_codes_map.keys()))
            if best_code and lang_codes_map.get(best_code) in available_langs:
                lang = lang_codes_map.get(best_code)
        except Exception:
            pass

    # 4/5) global defaults
    if not lang:
        lang = getattr(source_consts, 'GUI_LANGUAGE', app.config.get('DEFAULT_LANGUAGE', 'English'))
    
    return {
        '_': lambda idx: get_text(idx, lang),
        'texts': get_all_texts(lang),
        'current_lang': lang,
        'is_rtl': is_rtl(lang),
        'app_name': app_name,
        'user': {
            'first_name': session.get('first_name', ''),
            'last_name': session.get('last_name', ''),
            'username': session.get('username', '')
        } if 'username' in session else None
    }


# Main route
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


# API route for translations
@app.route('/api/i18n/<lang>')
def get_translations(lang):
    """Get all translations for a language"""
    return jsonify(get_all_texts(lang))


# API route to download PDF
@app.route('/api/download/<filename>')
def download_file(filename):
    """Download a generated file"""
    file_path = os.path.join('uploads', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    
    # Run development server
    app.run(debug=True, host='0.0.0.0', port=5000)
