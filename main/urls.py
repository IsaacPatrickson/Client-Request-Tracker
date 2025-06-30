from .views import *
from django.urls import path
from main.admin import custom_admin_site
# from django.contrib.auth.views import LogoutView

# URL patterns for the main app, routing HTTP requests to corresponding views:
# - 'admin/' uses the custom Django admin site instead of the default admin
# - '' (root) routes to the HomeView, the landing page for anonymous users
# - 'register/' routes to the user registration page
# - 'login/' routes to the custom login page with tailored authentication logic
# - 'logout/' uses Django's built-in LogoutView to log users out
# - 'account-disabled/' routes to a page informing users their account is disabled (e.g., non-staff users)

urlpatterns = [
    path('admin/', custom_admin_site.urls, name='custom_admin'),
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('account-disabled/', AccountDisabledView.as_view(), name='account_disabled')
]
