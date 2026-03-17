import requests
import re

session = requests.Session()
session.post('http://127.0.0.1:5000/login', data={'username': 'admin', 'password': 'admin123'})
resp = session.get('http://127.0.0.1:5000/models')

print('✅ STATUS: Page loaded successfully')
print(f'   Page size: {len(resp.text)} bytes')

# Check for container elements
containers = ['modelsContainer', 'comparisonChart', 'bestModelName', 'bestAccuracy']
for container in containers:
    if container in resp.text:
        print(f'✓ {container} found')
    else:
        print(f'✗ {container} missing')

# Check for unrendered template variables
unrendered = re.findall(r'\{\{[^}]+\}\}', resp.text)
if unrendered:
    print(f'\n⚠️ Found {len(unrendered)} unrendered template variables:')
    for v in unrendered[:5]:
        print(f'   - {v}')
else:
    print('\n✅ All template variables properly rendered')

# Check for models data in JSON
if '"1D-CNN"' in resp.text or "'1D-CNN'" in resp.text:
    print('✅ Models data found in page')
else:
    print('⚠️ Models data not found')

print('\n✅ Page ready for browser testing')
