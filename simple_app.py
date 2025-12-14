#!/usr/bin/env python3
"""
Simplified Factory Management System - Flask Backend
This version works without database for basic HTML serving
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
        'note': 'Simplified version without database',
        'endpoints': {
            'health': '/api/health',
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
    """Simple login endpoint for testing"""
    try:
        data = request.get_json()
        print(f"Login attempt: {data}")  # Debug output
        
        username = data.get('username')
        password = data.get('password')
        
        print(f"Username: {username}, Password: {password}")  # Debug output
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Simple hardcoded users for testing
        valid_users = {
            'admin': {'password': 'password', 'role': 'admin', 'full_name': 'System Administrator'},
            'manager': {'password': 'password', 'role': 'manager', 'full_name': 'Factory Manager'}
        }
        
        if username in valid_users and valid_users[username]['password'] == password:
            return jsonify({
                'access_token': f'token_{username}',  # Simple token for testing
                'user': {
                    'username': username,
                    'role': valid_users[username]['role'],
                    'full_name': valid_users[username]['full_name']
                }
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
    print("🏭 Factory Management System - Simplified Server")
    print("="*60)
    print(f"🚀 Server starting on http://localhost:{port}")
    print(f"📊 Environment: {'Development' if debug else 'Production'}")
    print("📝 Note: This is a simplified version without database")
    print("🌐 Frontend: http://localhost:5000")
    print("🔧 API: http://localhost:5000/api/health")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
