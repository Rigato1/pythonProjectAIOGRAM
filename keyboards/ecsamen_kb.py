from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON
from services.services import get_ecsamen


def get_ecsamen_kb(voprosy):
    btn1 = InlineKeyboardButton(
        text=voprosy[2],
        callback_data=str(voprosy[2]))
    btn2 = InlineKeyboardButton(
        text=voprosy[3],
        callback_data=str(voprosy[3]))
    btn3 = InlineKeyboardButton(
        text=voprosy[4],
        callback_data=str(voprosy[4]))
    btn4 = InlineKeyboardButton(
        text=voprosy[5],
        callback_data=str(voprosy[5]))
    ecsamen_kb = InlineKeyboardMarkup(
            inline_keyboard=[[btn1],
                        [btn2],
                        [btn3],
                        [btn4]],
        )
    return ecsamen_kb


vibrat_restart = InlineKeyboardButton(text='Начать текущий экзамен заново',
                                      callback_data=('restart'))

vibrat_druguyu_temu = InlineKeyboardButton(
    text='Выбрать другую тему',
    callback_data=('New_theme'))

ending_ecsamen_kb = InlineKeyboardMarkup(
    inline_keyboard=[[vibrat_restart],
                     [vibrat_druguyu_temu]])

