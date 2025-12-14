#!/usr/bin/env python3
"""
Test the login functionality
"""

import requests
import json

def test_login():
    """Test login with admin and manager credentials"""
    base_url = "http://localhost:5000"
    
    # Test admin login
    print("Testing admin login...")
    admin_data = {
        "username": "admin",
        "password": "password"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=admin_data)
        if response.status_code == 200:
            result = response.json()
            print(f"+ Admin login successful!")
            print(f"  Token: {result.get('access_token')}")
            print(f"  User: {result.get('user')}")
        else:
            print(f"- Admin login failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"- Admin login error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test manager login
    print("Testing manager login...")
    manager_data = {
        "username": "manager", 
        "password": "manager123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=manager_data)
        if response.status_code == 200:
            result = response.json()
            print(f"+ Manager login successful!")
            print(f"  Token: {result.get('access_token')}")
            print(f"  User: {result.get('user')}")
        else:
            print(f"- Manager login failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"- Manager login error: {e}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test invalid login
    print("Testing invalid login...")
    invalid_data = {
        "username": "admin",
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=invalid_data)
        if response.status_code == 401:
            print("+ Invalid login correctly rejected")
        else:
            print(f"- Invalid login should have been rejected: {response.status_code}")
    except Exception as e:
        print(f"- Invalid login test error: {e}")

def main():
    """Main test function"""
    print("=" * 60)
    print("Testing Login Functionality")
    print("=" * 60)
    print("Make sure the server is running first!")
    print("Run: py simple_app.py")
    print("=" * 60)
    
    test_login()
    
    print("\n" + "=" * 60)
    print("Login Test Complete")
    print("=" * 60)
    print("Valid credentials:")
    print("  Username: admin, Password: password")
    print("  Username: manager, Password: manager123")
    print("=" * 60)

if __name__ == "__main__":
    main()
