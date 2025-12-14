#!/usr/bin/env python3
"""
Test the working server login
"""

import requests
import json

def test_working_login():
    """Test login with the working server"""
    url = "http://localhost:5000/api/auth/login"
    
    print("Testing working server login...")
    
    # Test admin
    print("\n1. Testing admin login...")
    try:
        response = requests.post(url, json={'username': 'admin', 'password': 'password'})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test manager
    print("\n2. Testing manager login...")
    try:
        response = requests.post(url, json={'username': 'manager', 'password': 'manager123'})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test invalid
    print("\n3. Testing invalid login...")
    try:
        response = requests.post(url, json={'username': 'admin', 'password': 'wrong'})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_working_login()
