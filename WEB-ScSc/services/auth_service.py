import sqlite3
import hashlib
import os
from datetime import datetime


class AuthService:
    def __init__(self, db_path='data/users.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database with users table"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def signup(self, username, password, first_name, last_name, email=None):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self._hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, password_hash, first_name, last_name, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password_hash, first_name, last_name, email))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            return {
                'success': True,
                'user_id': user_id,
                'username': username
            }
        except sqlite3.IntegrityError:
            return {
                'success': False,
                'error': 'Username already exists'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def login(self, username, password):
        """Authenticate user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self._hash_password(password)
            
            cursor.execute('''
                SELECT id, username, first_name, last_name, email
                FROM users
                WHERE username = ? AND password_hash = ?
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'success': True,
                    'user': {
                        'id': user[0],
                        'username': user[1],
                        'first_name': user[2],
                        'last_name': user[3],
                        'email': user[4]
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'Invalid username or password'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user_by_username(self, username):
        """Get user information by username"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, first_name, last_name, email, created_at
                FROM users
                WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'first_name': user[2],
                    'last_name': user[3],
                    'email': user[4],
                    'created_at': user[5]
                }
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """Get user information by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, first_name, last_name, email, created_at
                FROM users
                WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'first_name': user[2],
                    'last_name': user[3],
                    'email': user[4],
                    'created_at': user[5]
                }
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
