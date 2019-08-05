import threading
import time

import schedule

from data.bot_starter import bot_el
from data.commands import weather_on_today
from data.models.model import get_weather_subscribers

cease_continuous_run = threading.Event()


class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):
        while not cease_continuous_run.is_set():
            schedule.run_pending()
            time.sleep(1)


def send_weather_for_subscribers():
    subscribers = get_weather_subscribers()
    for s in subscribers:
        time.sleep(0.1)  # so as not to exceed the limits of the telegram calls
        weather_on_today(bot_el, s.chat_id)


schedule.every().day.at('07:00').do(send_weather_for_subscribers)


def start_scheduler():
    continuous_thread = ScheduleThread()
    continuous_thread.start()
