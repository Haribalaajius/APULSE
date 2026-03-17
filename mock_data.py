"""
Mock Hardware Data Generator
Generates sample sensor readings to populate the dashboard without ESP32
"""
import requests
import time
import random
from datetime import datetime

# Target the Flask API
BASE_URL = "http://127.0.0.1:5000"
ADMIN_LOGIN = {"username": "admin", "password": "admin123"}

def login():
    """Login and return session"""
    session = requests.Session()
    resp = session.post(f"{BASE_URL}/login", data=ADMIN_LOGIN)
    if resp.status_code == 200:
        print("✅ Logged in successfully")
        return session
    else:
        print(f"❌ Login failed: {resp.status_code}")
        return None

def generate_mock_data():
    """Generate realistic mock sensor data"""
    base_voltage = 230  # Standard 230V supply
    base_current = 4500  # 4.5A nominal
    base_freq = 50  # 50Hz standard
    
    # Add some variation (±2%)
    voltage = base_voltage + random.uniform(-5, 5)
    current = base_current + random.uniform(-500, 500)
    frequency = base_freq + random.uniform(-0.5, 0.5)
    
    # Determine fault type (95% normal, 5% faults)
    fault_types = ['NORMAL'] * 19 + ['OVER_VOLTAGE', 'LOW_VOLTAGE', 'HIGH_CURRENT', 'FREQUENCY_SHIFT', 'PHASE_UNBALANCE']
    fault = random.choice(fault_types)
    
    if fault != 'NORMAL':
        # Make faulty readings more noticeable
        if fault == 'OVER_VOLTAGE':
            voltage = 250 + random.uniform(0, 20)
        elif fault == 'LOW_VOLTAGE':
            voltage = 200 + random.uniform(0, 10)
        elif fault == 'HIGH_CURRENT':
            current = 5500 + random.uniform(0, 1000)
        elif fault == 'FREQUENCY_SHIFT':
            frequency = base_freq + random.uniform(1, 3)
        elif fault == 'PHASE_UNBALANCE':
            current = 4500 + random.uniform(-2000, 2000)
    
    return {
        "voltage": round(voltage, 2),
        "current": round(current, 2),
        "frequency": round(frequency, 2),
        "fault": fault
    }

def main():
    print("🤖 Mock Hardware Data Generator")
    print("=" * 50)
    print("This generates sample data to populate the dashboard")
    print("without needing a physical ESP32 device.")
    print("=" * 50)
    
    # Login
    session = login()
    if not session:
        return
    
    print("\n📊 Generating mock sensor data...")
    print("Press CTRL+C to stop\n")
    
    count = 0
    try:
        while True:
            # Generate mock data
            data = generate_mock_data()
            
            # Send to Flask API
            resp = session.post(f"{BASE_URL}/api/hardware/data", json=data)
            
            count += 1
            status = "✅" if resp.status_code == 200 else "❌"
            print(f"{status} [{count}] {data['voltage']:.1f}V | {data['current']:.0f}mA | {data['frequency']:.1f}Hz | {data['fault']}")
            
            # Wait before next reading (simulate 2-second interval like test.py)
            time.sleep(2)
            
            # After 15 readings, user will see data on the dashboard
            if count == 15:
                print("\n✅ Dashboard should now have data!")
                print("   Open: http://localhost:5000/analytics")
                print("   Open: http://localhost:5000/alerts")
                print("\n📈 Continuing to generate data...\n")
    
    except KeyboardInterrupt:
        print(f"\n\n🛑 Stopped after {count} readings")
        print("Dashboard will retain this data")

if __name__ == "__main__":
    main()
