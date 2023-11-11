from telegram import ReplyKeyboardMarkup
from constants.texts import texts

start_keyboard_options = [
        [texts['run_query_button']],
    ]

def get_start_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(start_keyboard_options, one_time_keyboard=False, resize_keyboard=True)
    return markup
