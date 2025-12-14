#!/usr/bin/env python3
"""
Test script to verify HTML and Python backend connection
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import flask
        print("+ Flask imported successfully")
        
        import flask_sqlalchemy
        print("+ Flask-SQLAlchemy imported successfully")
        
        import flask_jwt_extended
        print("+ Flask-JWT-Extended imported successfully")
        
        import flask_cors
        print("+ Flask-CORS imported successfully")
        
        return True
    except ImportError as e:
        print(f"- Import error: {e}")
        return False

def test_app_creation():
    """Test if the Flask app can be created"""
    try:
        from app import app
        print("+ Flask app created successfully")
        
        # Test if the HTML route exists
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("+ HTML frontend route working")
            else:
                print(f"- HTML frontend route failed: {response.status_code}")
                
        # Test if the API route exists
        with app.test_client() as client:
            response = client.get('/api/health')
            if response.status_code == 200:
                print("+ API health endpoint working")
            else:
                print(f"- API health endpoint failed: {response.status_code}")
                
        return True
    except Exception as e:
        print(f"- App creation error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("Testing HTML and Python Backend Connection")
    print("=" * 50)
    
    # Test imports
    print("\n1. Testing imports...")
    if not test_imports():
        print("\n- Import test failed. Please install requirements:")
        print("   pip install -r requirements.txt")
        return False
    
    # Test app creation
    print("\n2. Testing app creation...")
    if not test_app_creation():
        print("\n- App creation test failed.")
        return False
    
    print("\n+ All tests passed!")
    print("\nTo run your application:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the server: python run.py")
    print("3. Open your browser to: http://localhost:5000")
    print("\nYour HTML frontend will be served at the root URL")
    print("Your API endpoints will be available at /api/*")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
