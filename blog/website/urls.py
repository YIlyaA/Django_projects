from django.urls import path
from website import views

app_name = "website"

urlpatterns = [
    path('', views.AllItemsView.as_view(), name='index'),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete'),
    path('myposts/', views.MyPostsView.as_view(), name='myposts'),
]
