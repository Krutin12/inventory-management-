"""
Run script for Factory Management System
"""

from app import app, init_db
import os

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Get configuration from environment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    # Run application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )