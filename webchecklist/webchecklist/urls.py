from django.contrib import admin
from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('admin/', admin.site.urls),   # rename for prod
    path('', include('secureapp.urls')),
    path('', include(tf_urls)),   # 2FA
]
