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
            "Ощущается как": data["current"]["feelslike_c"],
            "Скорость ветра": str(round(int(data["current"]["wind_kph"]) * 0.27778, 1)) + " м/с " + data["current"][
                "wind_dir"],
            "Осадки": data["current"]["condition"]["text"],
            "Давление": str(int(int(data["current"]["pressure_mb"]) * 0.75006)) + " мм рт.ст."
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
    hourly_forecast = []
    try:
        data = get_weather_today(city)
        city_name = data["location"]["name"]
        date = data["forecast"]["forecastday"][0]["date"]
        hourly_forecast.append(city_name)
        hourly_forecast.append(date)
        for hour_data in data["forecast"]["forecastday"][0]["hour"]:
            forecast = {
                "Местное время": hour_data["time"][-5:],
                "°С": hour_data["temp_c"],
                "Ощущается как": hour_data["feelslike_c"],
                "Скорость ветра": f"{round(hour_data['wind_kph'] * 0.27778, 1)} м/с {hour_data['wind_dir']}",
                "Осадки": hour_data["condition"]["text"],
                "Давление": f"{int(hour_data['pressure_mb'] * 0.75006)} мм рт.ст."
            }
            hourly_forecast.append(forecast)

        return hourly_forecast
    except HTTPException as e:
        raise e


@app.get("/weather/{city}/tomorrow")
async def weather_tomorrow(city: str):
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
                "Местное время": hour_data["time"][-5:],
                "°С": hour_data["temp_c"],
                "Ощущается как": hour_data["feelslike_c"],
                "Скорость ветра": f"{round(hour_data['wind_kph'] * 0.27778, 1)} м/с {hour_data['wind_dir']}",
                "Осадки": hour_data["condition"]["text"],
                "Давление": f"{int(hour_data['pressure_mb'] * 0.75006)} мм рт.ст."
            }
            hourly_forecast.append(forecast)

        return hourly_forecast
    except HTTPException as e:
        raise e


@app.get("/weather/{city}/week")
async def weather_week(city: str):
    """
    :param city:
    :return:
    Получить прогноз погоды на неделю вперёд (на 2 дня вперёд)
    """
    daily_forecast = []
    try:
        data = get_weather_not_today(city, 8)
        for day in data["forecast"]["forecastday"]:
            print(day["date"])
            forecast = {
                "День": day["date"],
                "Макс °С": day["day"]["maxtemp_c"],
                "Мин °С": day["day"]["mintemp_c"],
                "Средняя °С": day["day"]["avgtemp_c"],
                "Макс скорость ветра": str(round(day["day"]["maxwind_kph"] * 0.27778, 1)) + " м/c",
                "Описание": day["day"]["condition"]["text"],
                "Восход": day["astro"]["sunrise"],
                "Закат": day["astro"]["sunset"],

            }
            daily_forecast.append(forecast)

        return daily_forecast

    except HTTPException as e:
        raise e


@app.get("/weather/{city}/month")
async def weather_month(city: str):
    """
    Перестали отдавать по API данные с прогнозом более 2-х дней
    """
    pass
