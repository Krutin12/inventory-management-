#!/usr/bin/env python3
"""
Test login with the simple app directly
"""

from simple_app import app

def test_login():
    """Test login using Flask test client"""
    with app.test_client() as client:
        # Test admin login
        response = client.post('/api/auth/login', 
                             json={'username': 'admin', 'password': 'password'})
        print(f"Admin login status: {response.status_code}")
        print(f"Admin login response: {response.get_json()}")
        
        # Test manager login
        response = client.post('/api/auth/login', 
                             json={'username': 'manager', 'password': 'password'})
        print(f"Manager login status: {response.status_code}")
        print(f"Manager login response: {response.get_json()}")
        
        # Test invalid login
        response = client.post('/api/auth/login', 
                             json={'username': 'admin', 'password': 'wrong'})
        print(f"Invalid login status: {response.status_code}")
        print(f"Invalid login response: {response.get_json()}")

if __name__ == "__main__":
    test_login()
