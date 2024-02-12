from lexicon.lexicon import LEXICON
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


button_1 = KeyboardButton(text='Начать экзамен')

btn_stop = KeyboardButton(text='Остановить экзамен')
btn_restart = KeyboardButton(text='Начать текущий экзамен заново')


for_start_kb = ReplyKeyboardMarkup(keyboard=[[button_1]],
                                   resize_keyboard=True)

v_processe_kb = ReplyKeyboardMarkup(keyboard=[[btn_restart],
                                              [btn_stop]],resize_keyboard=True)




# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


