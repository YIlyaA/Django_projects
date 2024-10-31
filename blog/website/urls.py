from django.urls import path, include
from website import views

app_name = "website"

urlpatterns = [
    path('', views.AllItemsView.as_view(), name='index'),
]
