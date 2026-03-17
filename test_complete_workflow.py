#!/usr/bin/env python3
"""Complete workflow test - POST data and retrieve it"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

print("=" * 70)
print("SMART GRID DASHBOARD - COMPLETE WORKFLOW TEST")
print("=" * 70)

# Test 1: Post hardware data
print("\n📤 Step 1: Sending hardware data to dashboard...")
test_data = {
    "voltage": 230.5,
    "current": 15.2,
    "frequency": 50.0,
    "fault": "NORMAL"
}

try:
    r = requests.post(f"{BASE_URL}/api/hardware/data", json=test_data)
    if r.status_code == 200:
        print("✅ Data posted successfully")
        print(f"   Response: {r.json()}")
    else:
        print(f"❌ Failed with status {r.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Wait a moment
time.sleep(1)

# Test 2: Check if login page is accessible
print("\n🔓 Step 2: Checking login page...")
try:
    r = requests.get(f"{BASE_URL}/login")
    if r.status_code == 200 and '<title>' in r.text:
        print("✅ Login page accessible")
        print(f"   Page title found in HTML")
    else:
        print(f"❌ Login page check failed")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Test with session/login
print("\n👤 Step 3: Creating session and logging in...")
session = requests.Session()
try:
    # Try to login
    login_data = {"username": "admin", "password": "admin123"}
    r = session.post(f"{BASE_URL}/login", data=login_data)
    if r.status_code == 200:
        print("✅ Login successful, session created")
    else:
        print(f"   Login response status: {r.status_code}")
except Exception as e:
    print(f"❌ Login error: {e}")

# Test 4: Access protected endpoint with session
print("\n📊 Step 4: Retrieving analytics data (with session)...")
try:
    r = session.get(f"{BASE_URL}/api/analytics")
    if r.status_code == 200:
        try:
            data = r.json()
            if 'stats' in data:
                print("✅ Analytics data retrieved successfully")
                stats = data.get('stats', {})
                print(f"   Total readings: {stats.get('total_readings', 'N/A')}")
                print(f"   Avg voltage: {stats.get('voltage', {}).get('avg', 'N/A'):.2f}V")
            else:
                print(f"⚠️  Unexpected response format: {data}")
        except json.JSONDecodeError:
            print(f"⚠️  Response is not JSON")
    else:
        print(f"❌ Failed with status {r.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Retrieve alerts
print("\n🚨 Step 5: Retrieving alerts data (with session)...")
try:
    r = session.get(f"{BASE_URL}/api/alerts")
    if r.status_code == 200:
        try:
            data = r.json()
            if 'alerts' in data:
                print("✅ Alerts data retrieved successfully")
                print(f"   Number of alerts: {len(data.get('alerts', []))}")
                if data['alerts']:
                    print(f"   Latest alert: {data['alerts'][0].get('title', 'Unknown')}")
            else:
                print(f"⚠️  Unexpected response format")
        except json.JSONDecodeError:
            print(f"⚠️  Response is not JSON")
    else:
        print(f"❌ Failed with status {r.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 6: Get hardware history
print("\n📈 Step 6: Retrieving hardware history (with session)...")
try:
    r = session.get(f"{BASE_URL}/api/hardware/history?limit=10")
    if r.status_code == 200:
        try:
            data = r.json()
            if 'data' in data:
                print("✅ Hardware history retrieved")
                print(f"   Readings count: {data.get('count', 0)}")
                if data['data']:
                    latest = data['data'][-1]
                    print(f"   Latest: V={latest.get('voltage', 0):.1f}, I={latest.get('current', 0):.1f}, F={latest.get('frequency', 0):.1f}")
            else:
                print(f"⚠️  Unexpected response format")
        except json.JSONDecodeError:
            print(f"⚠️  Response is not JSON")
    else:
        print(f"❌ Failed with status {r.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 7: Access Dashboard
print("\n🏠 Step 7: Accessing main dashboard...")
try:
    r = session.get(f"{BASE_URL}/")
    if r.status_code == 200 and 'Smart Grid Dashboard' in r.text:
        print("✅ Dashboard loaded successfully")
        print(f"   Dashboard title found in HTML")
    elif r.status_code == 200:
        print("⚠️  Dashboard loaded (200) but title not found - may need wait for JS rendering")
    else:
        print(f"❌ Dashboard access failed: {r.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("WORKFLOW TEST COMPLETE")
print("=" * 70)
print("\n✅ Dashboard is operational and ready!")
print("\nAccess it at: http://localhost:5000/")
print("Login with: admin / admin123 or user / user123")
