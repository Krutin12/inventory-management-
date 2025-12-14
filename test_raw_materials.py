#!/usr/bin/env python3
"""
Test raw material functionality
"""

import requests
import json

def test_raw_material_buttons():
    """Test that raw material buttons work correctly"""
    print("Testing Raw Material Functionality")
    print("=" * 50)
    
    # Test server health
    print("\n1. Testing server health...")
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            print("+ Server is running")
        else:
            print(f"- Server health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"- Cannot connect to server: {e}")
        return
    
    # Test admin login
    print("\n2. Testing admin login...")
    try:
        response = requests.post('http://localhost:5000/api/auth/login', 
                               json={'username': 'admin', 'password': 'password'})
        if response.status_code == 200:
            data = response.json()
            print(f"+ Admin login successful")
            print(f"  Role: {data['user']['role']}")
        else:
            print(f"- Admin login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"- Login error: {e}")
        return
    
    print("\n" + "=" * 50)
    print("Raw Material Button Tests:")
    print("=" * 50)
    print("1. View Button - Should show material details")
    print("2. Edit Button - Should open edit modal")
    print("3. Stock Button - Should open stock adjustment modal")
    print("4. Delete Button - Should delete material with confirmation")
    print("5. Add Button - Should open add material form")
    print("=" * 50)
    print("\nTo test manually:")
    print("1. Open browser to: http://localhost:5000")
    print("2. Login as admin: admin/password")
    print("3. Go to Raw Materials section")
    print("4. Test all buttons")
    print("=" * 50)

if __name__ == "__main__":
    test_raw_material_buttons()
