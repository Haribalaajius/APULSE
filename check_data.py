import requests
import json

print('🔍 Checking Dashboard Data...\n')

# Check live data
try:
    resp = requests.get('http://127.0.0.1:5000/live-data')
    if resp.status_code == 200:
        data = resp.json()
        print('✅ Dashboard Metrics:')
        print(f'   Voltage: {data.get("voltage", "N/A")} V')
        print(f'   Current: {data.get("current", "N/A")} mA')
        print(f'   Frequency: {data.get("frequency", "N/A")} Hz')
        print(f'   Prediction: {data.get("prediction", "N/A")}')
    else:
        print('❌ /live-data failed')
except Exception as e:
    print(f'❌ Error: {e}')

# Check history
try:
    resp = requests.get('http://127.0.0.1:5000/api/hardware/history?limit=5')
    if resp.status_code == 200:
        history = resp.json()
        print(f'\n✅ Data History: {len(history)} readings stored')
    else:
        print('❌ /api/hardware/history failed')
except Exception as e:
    print(f'❌ Error: {e}')

# Check analytics
try:
    resp = requests.get('http://127.0.0.1:5000/api/analytics')
    if resp.status_code == 200:
        analytics = resp.json()
        print(f'\n✅ Analytics Data:')
        print(f'   Total readings: {analytics.get("total_readings", 0)}')
        print(f'   Avg voltage: {analytics.get("avg_voltage", 0):.1f} V')
        print(f'   Faults: {analytics.get("fault_count", 0)}')
    else:
        print('❌ /api/analytics failed')
except Exception as e:
    print(f'❌ Error: {e}')

# Check alerts
try:
    resp = requests.get('http://127.0.0.1:5000/api/alerts')
    if resp.status_code == 200:
        alerts = resp.json()
        print(f'\n✅ Alerts: {len(alerts)} total')
    else:
        print('❌ /api/alerts failed')
except Exception as e:
    print(f'❌ Error: {e}')
