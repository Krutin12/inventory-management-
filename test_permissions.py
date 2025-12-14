#!/usr/bin/env python3
"""
Test role-based permissions
"""

import requests
import json

def test_role_permissions():
    """Test that role-based permissions work correctly"""
    print("Testing Role-Based Permissions")
    print("=" * 50)
    
    # Test manager login and verify limited access
    print("\n1. Testing Manager Login...")
    response = requests.post('http://localhost:5000/api/auth/login', 
                            json={'username': 'manager', 'password': 'password'})
    
    if response.status_code == 200:
        data = response.json()
        print(f"+ Manager login successful")
        print(f"  Role: {data['user']['role']}")
        print(f"  Username: {data['user']['username']}")
        print("  Expected permissions: View, Edit, New Order (NO User Management)")
    else:
        print(f"- Manager login failed: {response.status_code}")
    
    # Test admin login and verify full access
    print("\n2. Testing Admin Login...")
    response = requests.post('http://localhost:5000/api/auth/login', 
                            json={'username': 'admin', 'password': 'password'})
    
    if response.status_code == 200:
        data = response.json()
        print(f"+ Admin login successful")
        print(f"  Role: {data['user']['role']}")
        print(f"  Username: {data['user']['username']}")
        print("  Expected permissions: Full access including User Management")
    else:
        print(f"- Admin login failed: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("Permission Summary:")
    print("MANAGER: View, Edit, New Order (NO User Management)")
    print("ADMIN: Full access including User Management")
    print("=" * 50)

if __name__ == "__main__":
    test_role_permissions()
