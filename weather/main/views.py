from django.shortcuts import render
import requests


# Create your views here.
def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=53294b3b0a37da5ccf0f7a5833d7ecb0"
    city = "Las Vegas"
    city_weather = requests.get(url.format(city)).json()
    print(city_weather)

    return render(request, "main/index.html")
