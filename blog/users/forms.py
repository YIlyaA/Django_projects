# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'username', 'phone', 'gender', 'password1', 'password2']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender not in dict(User.GENDERS):
            raise forms.ValidationError("Invalid gender selection.")
        return gender

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_username(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            return user.username  # Return the username for authentication
        except User.DoesNotExist:
            raise forms.ValidationError("This email is not registered.")    
