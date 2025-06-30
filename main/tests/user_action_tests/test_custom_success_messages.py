import pytest
from django.contrib.messages import get_messages

@pytest.mark.django_db
def test_login_success_message(client, django_user_model):
    user = django_user_model.objects.create_user(username='isaac', password='test123', is_staff=True)
    response = client.post('/login/', {'username': 'isaac', 'password': 'test123'}, follow=True)
    
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any("Welcome" in msg or "successfully logged in" in msg for msg in messages)

@pytest.mark.django_db
def test_register_success_message(client):
    response = client.post('/register/', {
        'username': 'newuser',
        'email': 'test@example.com',
        'password': 'strongpass123',
        'password_confirm': 'strongpass123'
    }, follow=True)
    
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any("successfully registered" in msg.lower() for msg in messages)