from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include("website.urls")),
    path('', include("users.urls")),
]
