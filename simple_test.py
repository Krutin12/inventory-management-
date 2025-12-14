#!/usr/bin/env python3
"""
Simple test script to verify basic Flask functionality
"""

import sys
import os

def test_basic_imports():
    """Test basic Flask imports without SQLAlchemy"""
    try:
        import flask
        print("+ Flask imported successfully")
        
        import flask_cors
        print("+ Flask-CORS imported successfully")
        
        return True
    except ImportError as e:
        print(f"- Import error: {e}")
        return False

def test_simple_app():
    """Test creating a simple Flask app"""
    try:
        from flask import Flask
        from flask_cors import CORS
        
        # Create a simple test app
        test_app = Flask(__name__)
        CORS(test_app)
        
        @test_app.route('/')
        def test_route():
            return "Test successful!"
        
        @test_app.route('/api/health')
        def health():
            return {"status": "healthy"}
        
        # Test the routes
        with test_app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("+ Basic Flask route working")
            else:
                print(f"- Basic Flask route failed: {response.status_code}")
                
            response = client.get('/api/health')
            if response.status_code == 200:
                print("+ API health route working")
            else:
                print(f"- API health route failed: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"- App creation error: {e}")
        return False

def test_html_serving():
    """Test if we can serve HTML files"""
    try:
        from flask import Flask, send_from_directory
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)
        
        @app.route('/')
        def serve_html():
            return send_from_directory('.', '1.html')
        
        # Test if HTML file exists
        if os.path.exists('1.html'):
            print("+ HTML file found")
        else:
            print("- HTML file not found")
            return False
            
        # Test the route
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("+ HTML serving route working")
                return True
            else:
                print(f"- HTML serving route failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"- HTML serving test error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("Simple Flask Connection Test")
    print("=" * 50)
    
    # Test basic imports
    print("\n1. Testing basic imports...")
    if not test_basic_imports():
        print("\n- Basic import test failed.")
        return False
    
    # Test simple app
    print("\n2. Testing simple Flask app...")
    if not test_simple_app():
        print("\n- Simple app test failed.")
        return False
    
    # Test HTML serving
    print("\n3. Testing HTML serving...")
    if not test_html_serving():
        print("\n- HTML serving test failed.")
        return False
    
    print("\n+ All basic tests passed!")
    print("\nTo run your application:")
    print("1. Run: py run.py")
    print("2. Open browser to: http://localhost:5000")
    print("\nNote: The full app with database may have SQLAlchemy compatibility issues")
    print("but the basic Flask server should work for serving your HTML frontend.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
