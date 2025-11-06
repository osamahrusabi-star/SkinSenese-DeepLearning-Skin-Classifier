from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()
u, created = User.objects.get_or_create(username='testuser', defaults={'email':'test@example.com'})
if created:
    u.set_password('Testpass123')
    u.save()
    print('created', created)

c = Client()
print('GET dashboard before login ->', c.get('/dashboard/').status_code)
resp = c.post('/login/', {'username': 'testuser', 'password': 'Testpass123'}, follow=True)
print('POST /login/ status', resp.status_code)
print('Final URL after follow:', resp.request.get('PATH_INFO'))
print('GET dashboard after login ->', c.get('/dashboard/').status_code)
