from .views import *
from django.urls import path
from main.admin import custom_admin_site
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', custom_admin_site.urls, name='custom_admin'),
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account-disabled/', AccountDisabledView.as_view(), name='account_disabled')
]
