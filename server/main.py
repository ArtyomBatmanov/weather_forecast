from fastapi import FastAPI, HTTPException, Request
from utils import get_weather_now, get_weather_today, get_weather_not_today
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # корневая директория проекта
app.mount("/static/", StaticFiles(directory=os.path.join(BASE_DIR, "client")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "client/"))


@app.get("/")
async def root(request: Request):
    """
    Отобразить прогноз погоды для Москвы на базовой странице.
    """
    # city = "Москва"
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/weather/{city}/now")
async def weather_now(request: Request, city: str):
    """
    :param city:
    :return:
    Получить прогноз погоды на данный момент
    """
    try:
        data = get_weather_now(city)

        forecast = {
            "city_name": data["location"]["name"],
            "local_time": data["location"]["localtime"][-6:],
            "temperature": data["current"]["temp_c"],
            "feels_like": data["current"]["feelslike_c"],
            "wind_speed": str(round(int(data["current"]["wind_kph"]) * 0.27778, 1)) + " м/с " + data["current"][
                "wind_dir"],
            "condition": data["current"]["condition"]["text"],
            "pressure": str(int(int(data["current"]["pressure_mb"]) * 0.75006)) + " мм рт.ст."
        }

        return templates.TemplateResponse("templates/now.html", {"request": request, "forecast": forecast})
    except HTTPException as e:
        raise e


@app.get("/api/weather/{city}/today")
async def weather_today(city: str, request: Request):
    """
    :param city:
    :return:
    Получить прогноз погоды на сегодня по часам
    """
    hourly_forecast = []
    try:
        data = get_weather_today(city)
        city_name = data["location"]["name"]
        date = data["forecast"]["forecastday"][0]["date"]
        hourly_forecast.append(city_name)
        hourly_forecast.append(date)
        for hour_data in data["forecast"]["forecastday"][0]["hour"]:
            forecast = {
                "local_time": hour_data["time"][-5:],
                "temperature": hour_data["temp_c"],
                "feels_like": hour_data["feelslike_c"],
                "wind_speed": f"{round(hour_data['wind_kph'] * 0.27778, 1)} м/с {hour_data['wind_dir']}",
                "condition": hour_data["condition"]["text"],
                "pressure": f"{int(hour_data['pressure_mb'] * 0.75006)} мм рт.ст."
            }
            hourly_forecast.append(forecast)

        return templates.TemplateResponse("templates/today.html", {"request": request, "forecast": hourly_forecast})
    except HTTPException as e:
        raise e


@app.get("/api/weather/{city}/tomorrow")
async def weather_tomorrow(city: str, request: Request):
    """
    :param city:
    :return:
    Получить прогноз погоды на завтра по часам
    """
    hourly_forecast = []
    try:
        data = get_weather_not_today(city, 2)
        city_name = data["location"]["name"]
        date = data["forecast"]["forecastday"][1]["date"]
        hourly_forecast.append(city_name)
        hourly_forecast.append(date)
        for hour_data in data["forecast"]["forecastday"][1]["hour"]:
            forecast = {
                "local_time": hour_data["time"][-5:],
                "temperature": hour_data["temp_c"],
                "feels_like": hour_data["feelslike_c"],
                "wind_speed": f"{round(hour_data['wind_kph'] * 0.27778, 1)} м/с {hour_data['wind_dir']}",
                "condition": hour_data["condition"]["text"],
                "pressure": f"{int(hour_data['pressure_mb'] * 0.75006)} мм рт.ст."
            }
            hourly_forecast.append(forecast)

        return templates.TemplateResponse("templates/tomorrow.html", {"request": request, "forecast": hourly_forecast})
    except HTTPException as e:
        raise e


@app.get("/api/weather/{city}/3-days/")
async def weather_week(city: str, request: Request):
    """
    :param city:
    :return:
    Получить прогноз погоды на 3 дня
    """
    daily_forecast = []
    try:
        data = get_weather_not_today(city, 8)
        for day in data["forecast"]["forecastday"]:
            print(day["date"])
            forecast = {
                "day": day["date"],
                "maxtemp_c": day["day"]["maxtemp_c"],
                "mintemp_c": day["day"]["mintemp_c"],
                "avgtemp_c °С": day["day"]["avgtemp_c"],
                "maxwind_kph": str(round(day["day"]["maxwind_kph"] * 0.27778, 1)) + " м/c",
                "text": day["day"]["condition"]["text"],
                "sunrise": day["astro"]["sunrise"],
                "sunset": day["astro"]["sunset"],

            }
            daily_forecast.append(forecast)

        return templates.TemplateResponse("templates/3_days.html", {"request": request, "forecast": daily_forecast})

    except HTTPException as e:
        raise e


@app.get("/api/weather/{city}/month")
async def weather_month(city: str):
    """
    Перестали отдавать по API данные с прогнозом более 2-х дней
    """
    pass
