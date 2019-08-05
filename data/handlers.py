import logging
from functools import wraps

from telegram import ChatAction

from data.commands import *
from data.models.model import update_user_location, set_user_subscribe
from data.properties import *

logger = logging.getLogger(__name__)


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(bot, update, *args, **kwargs):
        bot.send_chat_action(chat_id=update.message.chat.id, action=ChatAction.TYPING)

        return func(bot, update, *args, **kwargs)

    return command_func


@send_typing_action
def text_handler(bot, update):
    try:
        if update.message.text == WEATHER_TODAY_BUTTON_TEXT:
            weather_on_today(bot, update.message.chat.id)
        elif update.message.text == WEATHER_5_DAY_BUTTON_TEXT:
            weather_on_weak(bot, update.message.chat.id)
        elif update.message.text == HELP_BUTTON_TEXT:
            help_me(bot, update)
        elif update.message.text == PROFILE_BUTTON_TEXT:
            profile(bot, update)
        elif update.message.text == WEATHER_SUBSCRIBE_BUTTON_TEXT:
            subscribe(bot, update)
        else:
            bot.send_message(chat_id=update.message.chat.id, text="Наверное вы ошиблись")

    except UserWarning as error:
        bot.send_message(chat_id=update.message.chat.id, text=str(error))
        logger.error(error)
    except Exception as error:
        logger.error(error)
        raise


def sub_news(bot, update):
    set_user_subscribe(update.message.chat.id, True)
    update.message.reply_text(SUBSCRIPTION_ON)


def unsub_news(bot, update):
    set_user_subscribe(update.message.chat.id, False)
    update.message.reply_text(SUBSCRIPTION_OFF)


def location_handler(bot, update):
    user = get_user_by_chat_id(update.message.chat.id)

    keyboard = []

    if not user.is_home_ready:
        keyboard.append([InlineKeyboardButton("Установить домашнюю локацию",
                                              callback_data="home,lat:" + str(
                                                  update.message.location.latitude) + "|lon:" + str(
                                                  update.message.location.longitude))])
    else:
        keyboard.append([InlineKeyboardButton("Обновить домашнюю локацию",
                                              callback_data="home,lat:" + str(
                                                  update.message.location.latitude) + "|lon:" + str(
                                                  update.message.location.longitude))])

    keyboard.append([InlineKeyboardButton("Погода в регионе на сутки",
                                          callback_data="day,lat:" + str(
                                              update.message.location.latitude) + "|lon:" + str(
                                              update.message.location.longitude))])
    keyboard.append([InlineKeyboardButton("Погода на 6 дней",
                                          callback_data="week,lat:" + str(
                                              update.message.location.latitude) + "|lon:" + str(
                                              update.message.location.longitude))])

    update.message.reply_text("Выберите действие.", reply_markup=InlineKeyboardMarkup(keyboard))


def button(bot, update):
    try:
        chat_id = update.callback_query.message.chat.id
        print(update)
        query = update.callback_query
        elements = query.data.split(',')
        print(elements)
        if elements[0] == "home":
            coord = elements[1].split("|")
            update_user_location(chat_id=chat_id, lat=coord[0].split(":")[1], lon=coord[1].split(":")[1])
            HOME_DIRECTORY_REFRESH_TEXT = "Домашняя локация обновлена"
            update.callback_query.message.reply_text("%s" % HOME_DIRECTORY_REFRESH_TEXT)
        elif elements[0] == "day":
            coord = elements[1].split("|")
            weather_on_today(bot, chat_id, lat=coord[0].split(":")[1], lon=coord[1].split(":")[1])
        elif elements[0] == "week":
            coord = elements[1].split("|")
            weather_on_weak(bot, chat_id, lat=coord[0].split(":")[1], lon=coord[1].split(":")[1])
        elif elements[0] == "date":
            day = elements[1]
            coord = elements[2].split("|")
            weather_by_date(bot, chat_id, date=day, lat=coord[0].split(":")[1], lon=coord[1].split(":")[1])
        elif elements[0] == "sub":
            sub_news(bot, update.callback_query)
        elif elements[0] == "unsub":
            unsub_news(bot, update.callback_query)

    except Exception as er:
        print(er)
