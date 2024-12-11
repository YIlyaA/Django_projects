from django.shortcuts import render
import requests
from .forms import CityForm
from .models import City
import os


def index(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data["name"]
            if not City.objects.filter(name=city_name).exists():
                form.save()
            else:
                print("City already exists in the database")

    form = CityForm()
    cities = City.objects.all().order_by("-id")[:4]
    weather_data = []
    counter = 0
    for city in cities:
        counter += 1
        if counter >= 4:
            City.objects.filter(name=city).delete()
            continue
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}"
        city_weather = requests.get(
            url.format(city, os.environ.get("API_KEY"))
        ).json()  # request the API data and convert the JSON to Python data types
        if city_weather["cod"] == "404":
            City.objects.filter(name=city).delete()
            continue
        weather = {
            "name": city,
            "temperature": city_weather["main"]["temp"],
            "description": city_weather["weather"][0]["description"],
            "icon": city_weather["weather"][0]["icon"],
        }

        weather_data.append(weather)  # add the data for the current city into our list

    context = {"weather_data": weather_data, "form": form}
    return render(request, "main/index.html", context)
