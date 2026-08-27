import os
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_weather(city_name: str, forecast: bool, lang: str):
    type = "forecast" if forecast else "weather"
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/{type}?q={city_name}&appid={API_KEY}&lang={lang}&units=metric"
    )
    if response.status_code == 200:
        return response.json()


def get_weather_by_coords(lat: float, lon: float, lang: str):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&lang={lang}&units=metric"
    )
    if response.status_code == 200:
        return response.json()


def get_weather_data_by_coords(lat: float, lon: float, lang: str):
    weather_data = get_weather_by_coords(lat, lon, lang)
    if not weather_data:
        return (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )
    city_name = weather_data["name"]
    temp = round(weather_data["main"]["temp"])
    temp_min = round(weather_data["main"]["temp_min"])
    temp_max = round(weather_data["main"]["temp_max"])
    description = weather_data["weather"][0]["description"].capitalize()
    time_zone = timedelta(seconds=weather_data["timezone"])
    time = (datetime.now(timezone.utc) + time_zone).strftime("%H:%M")
    icon = weather_data["weather"][0]["icon"]
    return (
        city_name,
        temp,
        temp_min,
        temp_max,
        description,
        time_zone,
        time,
        icon,
    )


def get_weather_data(city_name, lang: str):
    weather_data = get_weather(city_name, False, lang)
    if not weather_data:
        return (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )
    temp = round(weather_data["main"]["temp"])
    temp_min = round(weather_data["main"]["temp_min"])
    temp_max = round(weather_data["main"]["temp_max"])
    description = weather_data["weather"][0]["description"].capitalize()
    time_zone = timedelta(seconds=weather_data["timezone"])
    time = (datetime.now(timezone.utc) + time_zone).strftime("%H:%M")
    icon = weather_data["weather"][0]["icon"]
    return temp, temp_min, temp_max, description, time_zone, time, icon


def get_forecast_data(city_name, lang: str):
    weather_data = get_weather(city_name, True, lang)
    if not weather_data:
        return [], None
    weather_list = []
    for weather in weather_data["list"]:
        weather_list.append(
            {
                "icon": weather["weather"][0]["icon"],
                "temp": round(weather["main"]["temp"]),
                "time": weather["dt_txt"][11:16],
            }
        )
    description = weather_data["list"][0]["weather"][0][
        "description"
    ].capitalize()
    return weather_list, description
