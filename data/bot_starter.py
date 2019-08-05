from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters

from data.commands import start, BOT_TOKEN
from data.handlers import button, text_handler, location_handler

updater = Updater(BOT_TOKEN)
bot_el = updater.bot


def bind_bot():
    add_handlers()
    updater.start_polling()
    updater.idle()


def add_handlers():
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.location, location_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
