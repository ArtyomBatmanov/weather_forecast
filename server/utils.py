from fastapi import HTTPException
import requests


API_KEY = "b40ef805679af68d2262431e6af0789a"
BASE_URL_NOW = "http://api.openweathermap.org/data/2.5/weather"
BASE_URL_TODAY = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}"
BASE_URL_GEOLOCATION = "http://api.openweathermap.org/geo/1.0/direct"




def get_weather_now(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    response = requests.get(BASE_URL_NOW, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"City not found or API error: {response.text}")



def get_weather_tomorrow(
        city: str,
        lat: str,
        lon: str,

):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    response = requests.get(BASE_URL_TODAY, params=params)

    if response.status_code == 200:
        return response.json
    else:
        raise HTTPException(status_code=response.status_code, detail="Что-то пошло не так")


def get_city_coordinates(city_name: str):
    params = {
        "q": city_name,
        # "limit": 1,  # Нам достаточно одного результата
        "appid": API_KEY
    }
    response = requests.get(BASE_URL_GEOLOCATION, params=params)

    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return data["lat"], data["lon"]
    else:
        raise HTTPException(status_code=404, detail="City not found")