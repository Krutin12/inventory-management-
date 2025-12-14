#!/usr/bin/env python3
"""
Working Factory Management System
This version has proper authentication
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# ===================== FRONTEND ROUTES =====================

@app.route('/')
def serve_frontend():
    """Serve the HTML frontend"""
    return send_from_directory('.', '1.html')

@app.route('/api')
def api_info():
    """API information endpoint"""
    return jsonify({
        'application': 'Factory Management System API',
        'version': '1.0.0',
        'status': 'running',
        'note': 'Working version with authentication',
        'endpoints': {
            'health': '/api/health',
            'login': '/api/auth/login',
            'info': '/api'
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Server is running',
        'version': '1.0.0'
    }), 200

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint with proper authentication"""
    try:
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Valid users with password "password"
        valid_users = {
            'admin': {'password': 'password', 'role': 'admin', 'full_name': 'System Administrator'},
            'manager': {'password': 'password', 'role': 'manager', 'full_name': 'Factory Manager'}
        }
        
        if username in valid_users and valid_users[username]['password'] == password:
            user_data = valid_users[username]
            return jsonify({
                'access_token': f'token_{username}',
                'user': {
                    'username': username,
                    'role': user_data['role'],
                    'full_name': user_data['full_name']
                },
                'message': f'Successfully logged in as {user_data["role"]}'
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===================== ERROR HANDLERS =====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ===================== MAIN ENTRY POINT =====================

if __name__ == '__main__':
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    print("\n" + "="*60)
    print("Factory Management System - WORKING VERSION")
    print("="*60)
    print(f"Server starting on http://localhost:{port}")
    print(f"Environment: {'Development' if debug else 'Production'}")
    print("Authentication: admin/password, manager/password")
    print("Frontend: http://localhost:5000")
    print("API: http://localhost:5000/api/health")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
