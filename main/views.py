from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .forms import UserRegistrationForm
from django.contrib.auth import logout


# Home view
class HomeView(TemplateView):
    template_name = 'home.html'
    
    # Logged in users should never see the home page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('admin:index'))
        return super().dispatch(request, *args, **kwargs)

# # Registration form view
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
    # Logged in users should never see the register page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('admin:index'))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    
# Custom login view
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    # Check if the user is_staff after a successful login
    # If not, call logout and redirect to account disabled
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            # Log the user out immediately
            logout(self.request)
            # Redirect to an account disabled or info page
            return redirect(reverse_lazy('account_disabled'))
        return super().form_valid(form)
    
    # Logged in users should never see the login page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect all logged-in users to the Django admin dashboard
            return redirect(reverse_lazy('admin:index'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # After successful login, send all users to Django admin dashboard
        return reverse_lazy('admin:index')
    
class AccountDisabledView(TemplateView):
    template_name = 'account-disabled.html'