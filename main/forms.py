from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group


class UserRegistrationForm (forms.ModelForm):
    # Explicitly declared fields usually display before the fields defined in class Meta
    email = forms.EmailField(
        widget=forms.EmailInput,
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        min_length=12,
        help_text='Required. Enter a secure password. Must be at least 12 characters.'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, 
        label='Confirm Password',
        required=True
    )
    
    class Meta:
        model = User
        # Moodel fields here
        fields = ['username', 'email']
        
    # The explicitly declared fields are reordered and put after the model fields
    field_order = ['username', 'email', 'password', 'password_confirm']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Passwords do not match')
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True
        if commit:
            user.save()
            try:
                limited_group = Group.objects.get(name='LimitedUsers')
                user.groups.add(limited_group)
            except Group.DoesNotExist:
                pass
        return user