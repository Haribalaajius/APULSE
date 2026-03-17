import requests

session = requests.Session()

# Login
login_resp = session.post('http://127.0.0.1:5000/login', 
                          data={'username': 'admin', 'password': 'admin123'})
print(f'Login: {login_resp.status_code}')

# Check each page
pages = ['analytics', 'models', 'alerts']

for page in pages:
    resp = session.get(f'http://127.0.0.1:5000/{page}')
    print(f'\n📄 {page.upper()} Page:')
    print(f'   Status: {resp.status_code}')
    print(f'   Size: {len(resp.text)} bytes')
    
    # Check for content
    if 'No data' in resp.text or 'no data' in resp.text:
        print('   ⚠️ Shows "no data" message')
    if 'container' in resp.text.lower():
        print('   ✓ Has container elements')
    if 'DOMContentLoaded' in resp.text or 'addEventListener' in resp.text:
        print('   ✓ Has JavaScript event listeners')
    
    # Check for data
    if page == 'models':
        if '"KNN"' in resp.text or "'KNN'" in resp.text:
            print('   ✓ Models data found')
        else:
            print('   ✗ Models data NOT found')
    elif page == 'analytics':
        if 'avgVolt' in resp.text or 'avgCurr' in resp.text:
            print('   ✓ Analytics elements found')
        else:
            print('   ✗ Analytics elements missing')
        if '/api/analytics' in resp.text:
            print('   ✓ API call to /api/analytics')
        else:
            print('   ✗ No API call found')

# Check if hardware data exists
print('\n📊 HARDWARE DATA:')
hw_resp = session.get('http://127.0.0.1:5000/api/hardware/history?limit=1')
data = hw_resp.json()
if data:
    print(f'   ✓ Hardware history exists: {len(data)} readings')
else:
    print('   ✗ Hardware history EMPTY - need to run test.py!')

# Check analytics API
print('\n⚙️ ANALYTICS API:')
analytics_resp = session.get('http://127.0.0.1:5000/api/analytics')
analytics = analytics_resp.json()
if analytics['stats']['total_readings'] > 0:
    print(f'   ✓ Analytics data available: {analytics["stats"]["total_readings"]} readings')
else:
    print(f'   ✗ Analytics data EMPTY')
    print(f'   Solution: Run python test.py in another terminal to collect hardware data!')
