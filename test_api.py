"""
Test the analyze_image endpoint to verify it works correctly
"""
import os
import sys
os.chdir(r"C:\Users\Osamah Mohammed\Desktop\django")
sys.path.insert(0, r"C:\Users\Osamah Mohammed\Desktop\django")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from io import BytesIO
from PIL import Image
import json

# Create test client
client = Client()

# Create test user
User = get_user_model()
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@test.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print("Test user created")
else:
    print("Test user already exists")

# Login
logged_in = client.login(username='testuser', password='testpass123')
print(f"Login successful: {logged_in}")

# Create a test image
img = Image.new('RGB', (224, 224), color='red')
img_io = BytesIO()
img.save(img_io, format='JPEG')
img_io.seek(0)
img_io.name = 'test.jpg'

# Test the analyze endpoint
print("\nTesting /api/analyze/ endpoint...")
response = client.post('/api/analyze/', {'image': img_io})

print(f"Status code: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")

if response.status_code == 200:
    try:
        data = json.loads(response.content)
        print("\nResponse data:")
        print(json.dumps(data, indent=2))
        
        # Check required fields
        required_fields = ['condition', 'confidence', 'risk_level', 'advice']
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            print(f"\nMissing fields: {missing}")
        else:
            print("\nAll required fields present!")
            print(f"  - Condition: {data['condition']}")
            print(f"  - Confidence: {data['confidence']}")
            print(f"  - Risk Level: {data['risk_level']}")
            print(f"  - Advice length: {len(data['advice'])} chars")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response content: {response.content[:500]}")
else:
    print(f"Error response: {response.content[:500]}")
