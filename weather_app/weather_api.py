import json
from django.core.cache import cache
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os
from dotenv import load_dotenv
load_dotenv()
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")

CACHE_TIMEOUT = 1800


@csrf_exempt
@require_http_methods(["GET"])
def get_weather(request):
    city_name = request.GET.get("city")
    url = f'https://api.weather.yandex.ru/v2/forecast?city={city_name}&lang=ru_RU'

    cached_weather_data = cache.get(city_name)

    if cached_weather_data:
        return JsonResponse(cached_weather_data)

    coordinates = get_coordinates(city_name)

    if coordinates is None:
        return JsonResponse({"error": "City not found"}, status=404)

    lat, lon = coordinates
    lang = request.GET.get("lang", "ru")
    limit = request.GET.get("limit", 1)
    hours = request.GET.get("hours", False)
    extra = request.GET.get("extra", False)

    headers = {
        "X-Yandex-API-Key": YANDEX_API_KEY,
    }

    params = {
        "lat": lat,
        "lon": lon,
        "lang": lang,
        "limit": limit,
        "hours": hours,
        "extra": extra,
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        weather_data = {
            "city": city_name,
            "temperature": response.json()["fact"]["temp"],
            "pressure": response.json()["fact"]["pressure_mm"],
            "wind_speed": response.json()["fact"]["wind_speed"],
        }

        cache.set(city_name, weather_data, CACHE_TIMEOUT)
        return JsonResponse(weather_data)
    else:
        return JsonResponse({"error": "Failed to fetch weather data"}, status=response.status_code)


def get_coordinates(city_name):
    with open("weather_app/city_coordinates.json", "r", encoding="utf-8") as json_file:
        unique_cities = json.load(json_file)

    city_info = unique_cities.get(city_name)

    if city_info:
        latitude = city_info["Широта"]
        longitude = city_info["Долгота"]
        return latitude, longitude
    else:
        return None
