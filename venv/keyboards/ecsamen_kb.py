from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import database
import random

def get_ecsamen_kb(voprosy, table):
    voprosy1=list(voprosy[2:6])
    if table == 'Мединский_курс_том_1' or 'Мединский_курс_том_2' or 'Мединский_курс_том_3':
        random.shuffle(voprosy1)
        btn1 = InlineKeyboardButton(
            text=voprosy1[0],
            callback_data=str(voprosy1[0]))
        btn2 = InlineKeyboardButton(
            text=voprosy1[1],
            callback_data=str(voprosy1[1]))
        btn3 = InlineKeyboardButton(
            text=voprosy1[2],
            callback_data=str(voprosy1[2]))
        btn4 = InlineKeyboardButton(
            text=voprosy1[3],
            callback_data=str(voprosy1[3]))
        ecsamen_kb = InlineKeyboardMarkup(
                inline_keyboard=[[btn1],
                            [btn2],
                            [btn3],
                            [btn4]],
            )
        return ecsamen_kb
    else:
        btn1 = InlineKeyboardButton(
            text=voprosy1[0],
            callback_data=str(voprosy1[0]))
        btn2 = InlineKeyboardButton(
            text=voprosy1[1],
            callback_data=str(voprosy1[1]))
        btn3 = InlineKeyboardButton(
            text=voprosy1[2],
            callback_data=str(voprosy1[2]))
        btn4 = InlineKeyboardButton(
            text=voprosy1[3],
            callback_data=str(voprosy1[3]))
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

