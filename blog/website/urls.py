from django.urls import path, include
from website import views

app_name = "website"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
