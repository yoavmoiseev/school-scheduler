from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Will be initialized by app.py
auth_service = None


def init_routes(auth_svc):
    global auth_service
    auth_service = auth_svc


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/signup')
def signup_page():
    """Render signup page"""
    if 'user_id' in session:
        return redirect('/')
    return render_template('signup.html')


@auth_bp.route('/login')
def login_page():
    """Render login page"""
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')


@auth_bp.route('/api/auth/signup', methods=['POST'])
def signup():
    """Handle user registration"""
    data = request.json
    
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    
    if not all([username, password, first_name, last_name]):
        return jsonify({
            'success': False,
            'error': 'Missing required fields'
        }), 400
    
    result = auth_service.signup(username, password, first_name, last_name, email)
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Handle user login"""
    data = request.json
    
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({
            'success': False,
            'error': 'Missing username or password'
        }), 400
    
    result = auth_service.login(username, password)
    
    if result['success']:
        # Set session
        session['user_id'] = result['user']['id']
        session['username'] = result['user']['username']
        session['first_name'] = result['user']['first_name']
        session['last_name'] = result['user']['last_name']
        session.permanent = True
        
        return jsonify(result)
    else:
        return jsonify(result), 401


@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    session.clear()
    return jsonify({'success': True})


@auth_bp.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current user information"""
    user = auth_service.get_user_by_id(session['user_id'])
    if user:
        return jsonify({
            'success': True,
            'user': user
        })
    else:
        session.clear()
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
