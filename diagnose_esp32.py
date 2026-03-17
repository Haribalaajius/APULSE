"""
ESP32 Diagnostic Tool
Helps identify and connect to your real ESP32 hardware
"""
import requests
import socket
import subprocess
import re
import time

def find_esp32_on_network():
    """Scan network for ESP32 devices"""
    print("\n🔍 Scanning network for ESP32...")
    print("=" * 60)
    
    # Try common ESP32 IP ranges (192.168.x.x)
    possible_ips = []
    
    # Get local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"Your Local IP: {local_ip}")
        
        # Extract subnet (e.g., 192.168.0)
        parts = local_ip.split('.')
        subnet = '.'.join(parts[:3])
        print(f"Scanning subnet: {subnet}.0/24\n")
        
        # Scan IPs in subnet
        for i in range(1, 255):
            ip = f"{subnet}.{i}"
            try:
                # Try to connect to ESP32 status endpoint
                resp = requests.get(f"http://{ip}/status", timeout=0.5)
                if resp.status_code == 200:
                    print(f"✅ Found device at {ip}")
                    print(f"   Response: {resp.text[:100]}")
                    possible_ips.append(ip)
            except:
                pass
    except Exception as e:
        print(f"Could not determine local IP: {e}")
    
    return possible_ips

def test_esp32_connection(ip):
    """Test if IP is reachable and returns sensor data"""
    print(f"\n🧪 Testing connection to {ip}...")
    print("-" * 60)
    
    try:
        # Test /status endpoint
        resp = requests.get(f"http://{ip}/status", timeout=3)
        print(f"✓ Status endpoint: {resp.status_code}")
        print(f"  Response:\n{resp.text}")
        
        # Parse data
        lines = [x.strip() for x in resp.text.replace("\r","").split("\n") if x.strip()]
        if len(lines) >= 3:
            print(f"\n✓ Sensor data found:")
            for line in lines[:3]:
                print(f"  - {line}")
            return True
        else:
            print(f"⚠️ Incomplete data (got {len(lines)} lines, need 3+)")
            return False
            
    except requests.exceptions.Timeout:
        print(f"✗ Timeout - Device not responding")
        return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Connection refused - Device unreachable")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_relay_control(ip):
    """Test relay control endpoints"""
    print(f"\n🔄 Testing relay control...")
    print("-" * 60)
    
    try:
        # Test FAULT relay (GPIO 1)
        resp1 = requests.get(f"http://{ip}/1", timeout=3)
        print(f"✓ FAULT relay (GPIO 1): {resp1.status_code}")
        
        time.sleep(0.5)
        
        # Test NORMAL relay (GPIO 2)
        resp2 = requests.get(f"http://{ip}/2", timeout=3)
        print(f"✓ NORMAL relay (GPIO 2): {resp2.status_code}")
        
        return True
    except Exception as e:
        print(f"✗ Relay control error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("    ESP32 Diagnostic Tool")
    print("="*60)
    
    print("\n📌 Quick Test:")
    print("Enter ESP32 IP (or press Enter to scan):")
    
    user_ip = input().strip()
    
    if user_ip:
        ips_to_test = [user_ip]
        print(f"\n✓ Using IP: {user_ip}")
    else:
        ips_to_test = find_esp32_on_network()
        
        if not ips_to_test:
            print("\n❌ No ESP32 devices found on network!")
            print("\nTroubleshooting:")
            print("1. Check if ESP32 is powered on")
            print("2. Check if ESP32 is connected to same WiFi network")
            print("3. Verify ESP32 IP address from your router")
            print("4. Check if firewall is blocking connections")
            return
    
    # Test each IP
    working_ips = []
    for ip in ips_to_test:
        if test_esp32_connection(ip):
            working_ips.append(ip)
            test_relay_control(ip)
    
    # Summary
    print("\n" + "="*60)
    print("    SUMMARY")
    print("="*60)
    
    if working_ips:
        print(f"\n✅ Found {len(working_ips)} working ESP32(s):")
        for ip in working_ips:
            print(f"   - {ip}")
        
        print("\n📝 Update your test.py with:")
        print(f'   ESP_IP = "{working_ips[0]}"')
        
        print("\n🚀 Next steps:")
        print("1. Update the ESP_IP in test.py")
        print("2. Keep Flask running: python app.py")
        print("3. Run: python test.py")
        print("4. Check dashboard at http://localhost:5000")
    else:
        print("\n❌ No working ESP32 found!")
        print("\nCommon issues:")
        print("1. ESP firmware may not have /status endpoint")
        print("2. Check ESP32 Arduino code")
        print("3. Verify HTTP server is running on ESP32")
        print("4. Check network connectivity")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAborted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
