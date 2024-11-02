from multiprocessing import context
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreationForm, CustomUserProfileForm
from django.contrib import messages
from django.urls import reverse_lazy
from users.mixins import RedirectAuthenticatedUserMixin
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class UserLoginView(RedirectAuthenticatedUserMixin, LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("website:index")

    def form_valid(self, form):
        messages.success(self.request, "Login successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid login credentials. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))


class UserRegisterView(RedirectAuthenticatedUserMixin, CreateView):
    models = User
    template_name = "users/register.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse_lazy("website:index")

    def form_valid(self, form):
        # form.save()                           # save the form
        user = form.save()  # save the form for user
        login(self.request, user)  # if you want login user without login again
        messages.success(self.request, "Registration successful. Please log in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Invalid registrations credentials. Please try again."
        )
        return self.render_to_response({"form": form})


class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = CustomUserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating profile. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Profile"
        context["genders"] = User.GENDERS
        return context