import requests
import re

session = requests.Session()
session.post('http://127.0.0.1:5000/login', data={'username': 'admin', 'password': 'admin123'})
resp = session.get('http://127.0.0.1:5000/models')

# Find script tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', resp.text, re.DOTALL)
if scripts:
    print(f"Found {len(scripts)} script tags\n")
    # Print the last script (should be the main one)
    for idx, script in enumerate(scripts):
        if 'models' in script.lower() or 'domcontentloaded' in script.lower():
            print(f"=== Script {idx} (first 800 chars) ===")
            print(script[:800])
            print("\n")
else:
    print("No script tags found")

# Also check if the template variables are rendering
if '{{' in resp.text:
    print("\n⚠️ WARNING: Template variables not rendered (found {{ in output)")
    # Find the problematic template variables
    import re
    unrendered = re.findall(r'\{\{[^}]+\}\}', resp.text)
    print(f"Found {len(unrendered)} unrendered template variables:")
    for var in unrendered[:5]:
        print(f"  - {var}")
