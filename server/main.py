from fastapi import FastAPI, HTTPException
from utils import get_weather_now, get_city_coordinates

app = FastAPI()


@app.get("/weather/{city}/now")
async def weather_now(city: str):
    try:
        data = get_weather_now(city)
        forecast = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        return forecast
    except HTTPException as e:
        raise e


@app.get("/weather/{city}/today")
async def weather_today(city: str):
    return "test"


@app.get("/weather/{city}/tomorrow")
async def weather_tomorrow(city: str):
    pass


@app.get("/weather/{city}/week")
async def weather_week(city: str):
    pass


@app.get("/weather/{city}/month")
async def weather_month(city: str):
    pass



