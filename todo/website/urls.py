from django.urls import path
from website import views

app_name = "website"

urlpatterns = [
    path('', views.ItemsView.as_view(), name="index"),
    path('delete/<int:pk>', views.DeleteItem.as_view(), name="delete"),
    path('update/<int:pk>', views.UpdateItem.as_view(), name="update"),
    # path('status/<int:pk>', views.UpdateItem.as_view(), name="status"),
]
