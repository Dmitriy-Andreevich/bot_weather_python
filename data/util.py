from datetime import datetime

import requests

from data.models.model import get_user_by_chat_id, User
from data.properties import *


def get_chat_user_with_location_or_none(chat_id) -> User:
    user = get_user_by_chat_id(chat_id)
    return user if user.is_home_ready else None


def get_user_valid_location(lat: float = None, lon: float = None, user=None) -> (float, float):
    if lat is not None and lon is not None:
        return lat, lon

    if user is None or not user.is_home_ready:
        raise UserWarning(
            "%s" % ERROR_HOME_LOCATION)
    else:
        return user.lat, user.lon


def get_icon_link(icon_name: str) -> str:
    return WEATHER_IMAGE_URL + icon_name + "@2x.png"


def get_modify_temp(temp: int) -> str:
    return '+' + str(temp) if temp > 0 else str(temp)


def send_get_weather_request(lat, lon) -> str:
    return requests.get(
        url=WEATHER_API_URL + "?lat=" + str(lat) + "&lon=" + str(
            lon) + "&appid=" + WEATHER_API_KEY + "&lang=ru&units=metric").json()


def get_days_from_response(req) -> dict:
    a = dict()
    for el in req['list']:
        key = datetime.fromtimestamp((el['dt'])).strftime('%d.%m')
        if key not in a:
            a[key] = []
        a[key].append(el)
    return a


def get_request_data(chat_id, lat, lon):
    user = get_user_by_chat_id(chat_id)
    req = send_get_weather_request(
        lat=user.lat if lat is None else lat,
        lon=user.lon if lon is None else lon
    )
    days: dict = get_days_from_response(req)
    return days, req, user
