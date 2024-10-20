from fastapi import FastAPI, HTTPException
from utils import get_weather_now, get_weather_today, get_weather_not_today

app = FastAPI()


@app.get("/weather/{city}/now")
async def weather_now(city: str):
    """
    :param city:
    :return:
    Получить прогноз погоды на данный момент
    """
    try:
        data = get_weather_now(city)

        forecast = {
            "Название города": data["location"]["name"],
            "Местное время": data["location"]["localtime"][-6:],
            "°С": data["current"]["temp_c"],
            "Скорость ветра": data["current"]["wind_kph"]
        }

        return forecast
    except HTTPException as e:
        raise e


@app.get("/weather/{city}/today")
async def weather_today(city: str):
    """
    :param city:
    :return:
    Получить прогноз погоды на сегодня по часам
    """

    try:
        data = get_weather_today(city)
        return data
    except HTTPException as e:
        raise e


@app.get("/weather/{city}/tomorrow")
async def weather_tomorrow(city: str):
    """
    :param city:
    :return:
    Получить прогноз погоды на завтра по часам
    """
    try:
        data = get_weather_not_today(city, 2)

        forecast = {
            "time": data["forecast"]["forecastday"][1]
        }
        return forecast
    except HTTPException as e:
        raise e


@app.get("/weather/{city}/week")
async def weather_week(city: str):
    """
    :param city:
    :return:
    Получить прогноз погоды на неделю вперёд
    """
    try:
        data = get_weather_not_today(city, 8)
        forecast = {
            "time": data["forecast"]["forecastday"]
        }

        return forecast

    except HTTPException as e:
        raise e


@app.get("/weather/{city}/month")
async def weather_month(city: str):
    pass
