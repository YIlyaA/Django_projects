from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from users.mixins import RedirectAuthenticatedUserMixin

User = get_user_model()

class UserLoginView(RedirectAuthenticatedUserMixin, LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('website:index')
    
    def form_valid(self, form):
        messages.success(self.request, 'Login successful.')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form)
        messages.error(self.request, 'Invalid login credentials. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))



class UserRegisterView(RedirectAuthenticatedUserMixin, CreateView):
    models = User
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = '/'  # Redirect to home page or another success page

    def form_valid(self, form):
        # form.save()          # save the form 
        user = form.save()                  # save the form for user
        login(self.request, user)           # if you want login user without login again 
        messages.success(self.request, 'Registration successful. Please log in.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid registrations credentials. Please try again.')
        return self.render_to_response({'form': form})



class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Successfully logged out.")
        return super().dispatch(request, *args, **kwargs)