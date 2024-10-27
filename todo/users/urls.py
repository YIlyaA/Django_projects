from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView

app_name = "users"

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
