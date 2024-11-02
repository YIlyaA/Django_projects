# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'username', 'phone', 'gender', 'password1', 'password2']

class CustomUserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'gender']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender not in dict(User.GENDERS):
            raise forms.ValidationError("Invalid gender selection.")
        return gender
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("Custom user with this Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

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
