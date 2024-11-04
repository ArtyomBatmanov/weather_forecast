from fastapi import HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL_NOW = "https://api.weatherapi.com/v1/current.json"
BASE_URL_TODAY = "https://api.weatherapi.com/v1/forecast.json"


def get_weather_now(city: str):
    params = {
        "q": city,
        "key": API_KEY,
    }

    response = requests.get(BASE_URL_NOW, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"City not found or API error: {response.text}")


def get_weather_today(
        city: str
):
    params = {
        "q": city,
        "key": API_KEY,
    }

    response = requests.get(BASE_URL_TODAY, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="WHY IS NOT WORKING????!!!")


def get_weather_not_today(
        city: str,
        days: int
):
    params = {
        "q": city,
        "key": API_KEY,
        "days": days
    }

    response = requests.get(BASE_URL_TODAY, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="WHY IS NOT WORKING????!!!")
