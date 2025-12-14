#!/usr/bin/env python3
"""
Debug login functionality
"""

import requests
import json

def test_login_api():
    """Test the login API directly"""
    url = "http://localhost:5000/api/auth/login"
    
    # Test data
    test_data = {
        "username": "admin",
        "password": "password"
    }
    
    print("Testing login API...")
    print(f"URL: {url}")
    print(f"Data: {test_data}")
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("Login successful!")
            print(f"Token: {data.get('access_token')}")
            print(f"User: {data.get('user')}")
        else:
            print("Login failed!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login_api()
