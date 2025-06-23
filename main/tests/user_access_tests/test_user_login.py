import pytest
from django.urls import reverse
from django.contrib.auth.models import User


# Tests cover login flow:
# - redirect for regular, staff, superuser users
# - login failure
# - access control for dashboards (authorized/unauthorized)

@pytest.mark.django_db
def test_user_without_is_staff_login_redirects_to_account_disabled_message(client):
    # Create a user wihtout is_staff 
    # This should never happen on account registration
    # Only occurs if another admin has altered permissions and disabled is_staff 
    # Effectively deactivating the account 
    User.objects.create_user(username='newuser', password='password123', is_staff=False)
    # Post login credentials
    url = reverse('login')
    response = client.post(url, {
        'username': 'newuser',
        'password': 'password123',
    })
    assert response.status_code == 302
    assert response.url == reverse('account_disabled')

@pytest.mark.django_db
def test_is_staff_user_login_redirects_to_admin_dashboard(client):
    # Test redirect after login for staff user
    # Create staff user
    User.objects.create_user(username='adminuser', password='adminpass123', is_staff=True)
    url = reverse('login')
    response = client.post(url, {
        'username': 'adminuser',
        'password': 'adminpass123',
    })
    assert response.status_code == 302
    assert response.url == reverse('admin:index')

@pytest.mark.django_db
def test_superuser_login_redirects_to_admin_dashboard(client):
    # Test redirect after login for superuser
    # Create superuser
    User.objects.create_superuser(username='superuser', password='superpass123')
    url = reverse('login')
    response = client.post(url, {
        'username': 'superuser',
        'password': 'superpass123',
    })
    assert response.status_code == 302
    assert response.url == reverse('admin:index')

@pytest.mark.django_db
def test_login_fails_with_wrong_password(client):
    # Tests login failure with incorrect password
    User.objects.create_user(username='newuser', password='password123', is_staff=True)
    url = reverse('login')
    response = client.post(url, {
        'username': 'newuser',
        'password': 'wrongpassword',
    })
    # Login form re-rendered with error
    assert response.status_code == 200
    assert b"Please enter a correct username and password" in response.content
    
@pytest.mark.django_db
def test_homeview_redirects_authenticated(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='pass', is_staff=True)
    client.force_login(user)

    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('admin:index')

@pytest.mark.django_db
def test_registerview_redirects_authenticated(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='pass', is_staff=True)
    client.force_login(user)

    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('admin:index')