import datetime

from pony.orm import *

from data.models.db_starter import db


class User(db.Entity):
    chat_id = Required(int)
    lat = Required(float, default=0.0)
    lon = Required(float, default=0.0)
    is_sub = Optional(bool, default=False)
    is_home_ready = Optional(bool, default=False)
    create_time = Required(datetime.datetime, default=datetime.datetime.utcnow)
    update_time = Required(datetime.datetime, default=datetime.datetime.utcnow)


db.generate_mapping(create_tables=True)


@db_session
def add_user_if_not_exist(chat_id: LongStr) -> User:
    user = User.get(chat_id=chat_id)
    if user is None:
        user = User(chat_id=chat_id, lat=0, lon=0, is_sub=False, is_home_ready=False)
    return user


@db_session
def get_user_by_chat_id(chat_id) -> User:
    return User.get(chat_id=chat_id)


@db_session
def update_user_location(chat_id, lat, lon) -> User:
    return User.get(chat_id=chat_id).set(lat=lat, lon=lon, is_home_ready=True, update_time=datetime.datetime.utcnow())


@db_session
def set_user_subscribe(chat_id, status: bool) -> User:
    return User.get(chat_id=chat_id).set(is_sub=status, update_time=datetime.datetime.utcnow())


@db_session
def get_weather_subscribers() -> list:
    return list(User.select(lambda el: el.is_sub is True and el.is_home_ready is True))
