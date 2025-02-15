from django.urls import path
from website import views

app_name = "website"

urlpatterns = [
    path('', views.AllItemsView.as_view(), name='index'),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete'),
    path('update/<int:pk>/', views.UpdatePostView.as_view(), name='update'),
    path('create/', views.CreatePostView.as_view(), name='create'),
    path('myposts/', views.MyPostsView.as_view(), name='myposts'),
    path('post/<int:pk>', views.BlogPostDetailView.as_view(), name='detail'),
]
