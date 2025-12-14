#!/usr/bin/env python3
"""
Test role validation to ensure manager cannot login as admin
"""

import requests
import json

def test_role_validation():
    """Test that role validation works correctly"""
    url = "http://localhost:5000/api/auth/login"
    
    print("Testing Role Validation")
    print("=" * 50)
    
    # Test 1: Manager login should return manager role
    print("\n1. Testing manager login...")
    response = requests.post(url, json={'username': 'manager', 'password': 'password'})
    if response.status_code == 200:
        data = response.json()
        print(f"+ Manager login successful")
        print(f"  Role: {data['user']['role']}")
        print(f"  Username: {data['user']['username']}")
        if data['user']['role'] == 'manager':
            print("+ Role is correctly set to 'manager'")
        else:
            print(f"- Role mismatch! Expected 'manager', got '{data['user']['role']}'")
    else:
        print(f"- Manager login failed: {response.status_code}")
    
    # Test 2: Admin login should return admin role
    print("\n2. Testing admin login...")
    response = requests.post(url, json={'username': 'admin', 'password': 'password'})
    if response.status_code == 200:
        data = response.json()
        print(f"+ Admin login successful")
        print(f"  Role: {data['user']['role']}")
        print(f"  Username: {data['user']['username']}")
        if data['user']['role'] == 'admin':
            print("+ Role is correctly set to 'admin'")
        else:
            print(f"- Role mismatch! Expected 'admin', got '{data['user']['role']}'")
    else:
        print(f"- Admin login failed: {response.status_code}")
    
    # Test 3: Invalid user should fail
    print("\n3. Testing invalid user...")
    response = requests.post(url, json={'username': 'invalid', 'password': 'password'})
    if response.status_code == 401:
        print("+ Invalid user correctly rejected")
    else:
        print(f"- Invalid user should have been rejected: {response.status_code}")

if __name__ == "__main__":
    test_role_validation()
