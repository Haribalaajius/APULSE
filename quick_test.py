#!/usr/bin/env python3
import requests

BASE_URL = "http://localhost:5000"

print("Testing /api/hardware/data POST...")
r = requests.post(f"{BASE_URL}/api/hardware/data", json={"voltage": 230, "current": 15, "frequency": 50, "fault": "NORMAL"})
print(f"Status: {r.status_code}, Content: '{r.text[:100]}'")

print("\nTesting /api/analytics GET...")
r = requests.get(f"{BASE_URL}/api/analytics")
print(f"Status: {r.status_code}, Content: '{r.text[:100]}'")

print("\nTesting /api/alerts GET...")
r = requests.get(f"{BASE_URL}/api/alerts")
print(f"Status: {r.status_code}, Content: '{r.text[:100]}'")

print("\nTesting / GET (no session)...")
r = requests.get(f"{BASE_URL}/")
print(f"Status: {r.status_code}, Content: '{r.text[:100]}'")

print("\nTesting /login GET...")
r = requests.get(f"{BASE_URL}/login")
print(f"Status: {r.status_code}, HTML title: {'<title>' in r.text}")

