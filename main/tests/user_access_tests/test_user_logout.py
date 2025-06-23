import pytest
from django.urls import reverse
from django.contrib.auth.models import User

# Tests logout behavior:
# - logout success and redirect
# - after logout, protected page access redirects to login

@pytest.mark.django_db
def test_user_can_logout_successfully(client):
    # Create and log in a test user
    user = User.objects.create_user(username='testuser', password='testpass123')
    logged_in = client.login(username='testuser', password='testpass123')
    assert logged_in is True  # Ensure login was successful
    # Hit the logout URL
    logout_url = reverse('logout')  # assuming you have the URL named 'logout'
    response = client.post(logout_url, follow=True)  # follow redirects
    # Check that after logout user is redirected (typically to login page or home)
    assert response.status_code == 200
    # Check redirect target URL is the login page
    assert response.redirect_chain[-1][0].endswith(reverse('login'))
    # Confirm user is logged out: accessing a login-required page should redirect to login
    dashboard_url = reverse('admin:index')  # protected page
    response2 = client.post(dashboard_url)
    assert response2.status_code == 302  # Redirect to login
    assert reverse('login') in response2.url
