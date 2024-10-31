from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class RedirectAuthenticatedUserMixin(AccessMixin):
    """Миксин для редиректа аутентифицированных пользователей с защищенных страниц"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('website:index')  # или на любую другую страницу
        return super().dispatch(request, *args, **kwargs)
