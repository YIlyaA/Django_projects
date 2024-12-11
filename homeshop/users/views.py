from email import message
from django.contrib.auth.decorators import login_required
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy

from orders.models import Order, OrderItem
from carts.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.db.models import Prefetch


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    # success_url = reverse_lazy('main:index')  $ instead of get_success_url()

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("user:logout"):
            return redirect_page
        return reverse_lazy("main:index")

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                # delete old authorized user carts
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # add new authorized user carts from anonimous session
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(self.request, f"{user.username}, You are logged in")

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Authorisation"
        return context


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("user:profile")

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"{user.username}, registration was successful")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Registration"
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Кабинет'
        context['orders'] =Order.objects.filter(user=self.request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).order_by("-id")
        return context


class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Корзина'
        return context
    

# class UserLogoutView(LoginRequiredMixin, TemplateView):
#     template_name = 'users/logout.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Home - Выход'
#         return context

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             session_key = request.session.session_key
#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f"{username}, Вы вошли в аккаунт")
#                 if session_key:
#                     # delete old authorized user carts
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                     # add new authorized user carts from anonimous session
#                     Cart.objects.filter(session_key=session_key).update(user=user)
#                 redirect_page = request.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('user:logout'):
#                     return HttpResponseRedirect(request.POST.get('next'))

#                 return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'Home - Авторизация',
#         'form': form
#     }
#     return render(request, 'users/login.html', context)


# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()

#             session_key = (
#                 request.session.session_key
#             )  # чтобы корзина не сбрасывалась для незарег пользователя

#             user = form.instance
#             auth.login(request, user)

#             if session_key:  # чтобы корзина не сбрасывалась для незарег пользователя
#                 Cart.objects.filter(session_key=session_key).update(
#                     user=user
#                 )  # чтобы корзина не сбрасывалась для незарег пользователя

#             messages.success(request, f"{user.username}, registration was successful")
#             return HttpResponseRedirect(
#                 reverse("main:index")
#             )  # Функция reverse преобразует 'main:index' в url и перенаправляет
#     else:
#         form = UserRegistrationForm()

#     context = {"title": "Home - registration", "form": form}
#     return render(request, "users/registration.html", context)


# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = ProfileForm(
#             data=request.POST, instance=request.user, files=request.FILES
#         )
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile was updated successfully")
#             return HttpResponseRedirect(
#                 reverse("users:profile")
#             )  # Функция reverse преобразует 'main:index' в url и перенаправляет
#     else:
#         form = UserRegistrationForm(instance=request.user)

#     orders = (
#         Order.objects.filter(user=request.user)
#         .prefetch_related(
#             Prefetch(
#                 "orderitem_set",
#                 queryset=OrderItem.objects.select_related("product"),
#             )
#         )
#         .order_by("-id")
#     )

#     context = {
#         "title": "Home - profile",
#         "form": form,
#         "orders": orders,
#     }
#     return render(request, "users/profile.html", context)


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, successfully logout")
    auth.logout(request)
    return redirect(reverse("main:index"))


# def users_cart(request):
#     return render(request, "users/users_cart.html")
