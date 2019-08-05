from datetime import datetime

import numpy
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from data.image_drawer import create_weather_image
from data.models.model import add_user_if_not_exist, get_user_by_chat_id
from data.properties import *
from data.util import get_request_data, get_user_valid_location


def start(bot, update):
    add_user_if_not_exist(update.message.chat.id)
    kk = [[WEATHER_TODAY_BUTTON_TEXT, WEATHER_5_DAY_BUTTON_TEXT],
          [PROFILE_BUTTON_TEXT, HELP_BUTTON_TEXT],
          [WEATHER_SUBSCRIBE_BUTTON_TEXT]]
    bot.send_message(chat_id=update.message.chat.id,
                     text='Привет, {}'.format(
                         update.message.from_user.first_name) + '.\nПожалуйста, выбери команду на клавиатуре снизу',
                     reply_markup=ReplyKeyboardMarkup(kk))


def subscribe(bot, update):
    user = get_user_by_chat_id(update.message.chat.id)
    try:
        but = [InlineKeyboardButton("Отписаться", callback_data="unsub")] if user.is_sub else [InlineKeyboardButton("Подписаться", callback_data="sub")]

        update.message.reply_text(SUBSCRIBE_CALL_TEXT)
        update.message.reply_text(text="Статус вашей подписки: " + ("активна" if user.is_sub else "не активирована"), reply_markup=InlineKeyboardMarkup([but]))
    except Exception as er:
        print(er)


def profile(bot, update):
    user = get_user_by_chat_id(update.message.chat.id)

    update.message.reply_text(
        "Здравствуйте, " + update.message.chat.first_name + " " + update.message.chat.last_name +
        "\nИнформация о вашем аккаунте:"
        "\nСтатус подписки на функцию \"Погода утром\" : " + (
            "подписан " if user.is_sub else "не подписан") +
        "\nВаша домашняя геолокация: " + ("" if user.is_home_ready else "не установлено"))

    if user.is_home_ready:
        bot.sendLocation(update.message.chat.id, user.lat, user.lon)
        update.message.reply_text(
            CHANGE_LOCATION_TEXT)


def weather_on_today(bot, chat_id: int, lat=None, lon=None):
    days, req, user = request_validation(chat_id, lat, lon)
    date = datetime.now().strftime('%d.%m')
    sequence_array = numpy.concatenate(list(days.values()), axis=None)[:8]
    update_mess = bot.send_message(chat_id=chat_id,
                                   text='Загрузка погоды в ' + req['city'][
                                       'name'] + ' на ближайшие сутки [' + date + ']...')
    bot.send_photo(chat_id=chat_id, photo=create_weather_image([sequence_array]))
    update_mess.edit_text("Погода в " + req['city']['name'] + " на " + date)


def weather_on_weak(bot, chat_id: int, lat=None, lon=None):
    days, req, user = request_validation(chat_id, lat, lon)
    keyboard = get_weak_keyboard(days, user, lat, lon)

    update_mess = bot.send_message(chat_id=chat_id,
                                   text='Загрузка погоды в ' + req['city']['name'] + ' на 6 дней...')
    bot.send_photo(chat_id=chat_id, photo=create_weather_image(days.values()),
                   reply_markup=InlineKeyboardMarkup(keyboard))
    update_mess.edit_text("Погода в " + req['city']['name'] + " на 6 дней")


def weather_by_date(bot, chat_id: int, date: str, lat=None, lon=None):
    days, req, user = request_validation(chat_id, lat, lon)
    update_mess = bot.send_message(chat_id=chat_id,
                                   text='Загрузка погоды в ' + req['city']['name'] + ' на ' + date + ' ...')
    bot.send_photo(chat_id=chat_id, photo=create_weather_image([days[date]]))
    update_mess.edit_text("Погода в " + req['city']['name'] + " на " + date)


def request_validation(chat_id, lat, lon):
    valid_lat, valid_lon = get_user_valid_location(lat, lon, user=get_user_by_chat_id(chat_id))
    days, req, user = get_request_data(chat_id, valid_lat, valid_lon)
    return days, req, user


def get_weak_keyboard(days, user, lat=None, lon=None) -> map:
    return map(lambda v: [InlineKeyboardButton(v, callback_data="date," + v + ",lat:" + str(
        user.lat if lat is None else lat) + "|lon:" + str(
        user.lon if lon is None else lon))], days.keys())


def help_me(bot, update):
    update.message.reply_text("Информация об основных функциях бота")
