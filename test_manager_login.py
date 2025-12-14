#!/usr/bin/env python3
"""
Test manager login specifically
"""

import requests
import json

def test_manager_login():
    """Test manager login in detail"""
    url = "http://localhost:5000/api/auth/login"
    
    print("=" * 60)
    print("Testing Manager Login")
    print("=" * 60)
    
    # Test manager login
    manager_data = {
        "username": "manager",
        "password": "password"
    }
    
    print(f"\n1. Sending login request...")
    print(f"   URL: {url}")
    print(f"   Data: {manager_data}")
    
    try:
        response = requests.post(url, json=manager_data)
        
        print(f"\n2. Response received:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"   Response Body: {json.dumps(response_data, indent=2)}")
        except:
            print(f"   Response Body (raw): {response.text}")
        
        if response.status_code == 200:
            data = response_data if 'response_data' in locals() else response.json()
            if 'access_token' in data:
                print(f"\n✅ Login SUCCESSFUL!")
                print(f"   Role: {data.get('user', {}).get('role')}")
                print(f"   User: {data.get('user', {}).get('full_name')}")
            else:
                print(f"\n❌ Login FAILED - No access token")
        else:
            print(f"\n❌ Login FAILED - Status {response.status_code}")
            if 'response_data' in locals():
                print(f"   Error: {response_data.get('error', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("   Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_manager_login()

