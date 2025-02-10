from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def register(request):
    return render(request, "register.html")


def dashboard(request):
    return render(request, "dashboard.html")