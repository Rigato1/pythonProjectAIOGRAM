from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_COMMANDS


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
        description in LEXICON_COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)

# Создаем объекты кнопок
#button_1 = KeyboardButton(text='Собак 🦮')
#button_2 = KeyboardButton(text='Огурцов 🥒')

# Создаем объект клавиатуры, добавляя в него кнопки
#keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]])
#prodoljit=KeyboardButton(text='')

def get_main_keyboard():
    pass