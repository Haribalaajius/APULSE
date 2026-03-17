#!/usr/bin/env python3
"""Test script to verify all dashboard endpoints are working"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

# Test data
test_hardware_data = {
    "voltage": 230.5,
    "current": 15.2,
    "frequency": 50.0,
    "fault": "NORMAL"
}

def test_endpoints():
    """Test all endpoints"""
    
    print("=" * 60)
    print("TESTING DASHBOARD ENDPOINTS")
    print("=" * 60)
    
    # 1. Test hardware data reception (no auth required)
    print("\n1. Testing /api/hardware/data (POST - no auth)...")
    try:
        response = requests.post(f"{BASE_URL}/api/hardware/data", json=test_hardware_data, timeout=2)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    time.sleep(1)
    
    # 2. Test live data endpoint (requires auth)
    print("\n2. Testing /live-data (GET - requires auth)...")
    try:
        response = requests.get(f"{BASE_URL}/live-data", timeout=2)
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
            print(f"   Redirected to login (expected for non-authenticated request)")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Test analytics API (requires auth)
    print("\n3. Testing /api/analytics (GET - requires auth)...")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics", timeout=2)
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
            print(f"   Redirected to login (expected for non-authenticated request)")
        else:
            print(f"   Response: {json.dumps(response.json(), indent=2)[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Test alerts API (requires auth)
    print("\n4. Testing /api/alerts (GET - requires auth)...")
    try:
        response = requests.get(f"{BASE_URL}/api/alerts", timeout=2)
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
            print(f"   Redirected to login (expected for non-authenticated request)")
        else:
            print(f"   Response: {json.dumps(response.json(), indent=2)[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Test hardware history
    print("\n5. Testing /api/hardware/history (GET - requires auth)...")
    try:
        response = requests.get(f"{BASE_URL}/api/hardware/history", timeout=2)
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
            print(f"   Redirected to login (expected for non-authenticated request)")
        else:
            print(f"   Response: {json.dumps(response.json(), indent=2)[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("ENDPOINT TESTS COMPLETE")
    print("=" * 60)
    print("\nNote: Authenticated endpoints should redirect to /login")
    print("This is normal behavior.")

if __name__ == "__main__":
    test_endpoints()
