from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .models import CustomUser
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView


class UserRegistrationView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)  # login user without login again 
        messages.success(self.request, 'Registration successful. Please log in.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid registrations credentials. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))
    

class UserLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('website:index')
    
    def form_valid(self, form):
        messages.success(self.request, 'Login successful.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login credentials. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Successfully logged out.")
        return super().dispatch(request, *args, **kwargs)
 
    def get_success_url(self):
        return reverse_lazy('users:login')
