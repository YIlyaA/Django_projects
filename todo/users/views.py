# from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from .mixins import RedirectAuthenticatedUserMixin

class UserRegistrationView(RedirectAuthenticatedUserMixin, CreateView):
    model = CustomUser                              # users model 
    form_class = CustomUserCreationForm             # registration form
    template_name = 'users/register.html'           # template name
    success_url = reverse_lazy('users:login')       # success url

    def form_valid(self, form):
        form.save()          # save the form 
        # user = form.save()                  # save the form for user
        # login(self.request, user)           # if you want login user without login again 
        messages.success(self.request, 'Registration successful. Please log in.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid registrations credentials. Please try again.')
        return super().form_invalid(form)
    

class UserLoginView(RedirectAuthenticatedUserMixin, LoginView):
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
    def get_success_url(self):
        return reverse_lazy('users:login')  # Redirects to the login page after logout

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Successfully logged out.")
        return super().dispatch(request, *args, **kwargs)