from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db, check_users, vivod_dannih
from keyboards.knopki_urokov import for_start_kb
from keyboards.ecsamen_kb import get_ecsamen_kb, ending_ecsamen_kb
from lexicon.lexicon import LEXICON
from services.services import get_ecsamen, zagruzka_dannih, kolichestvo_voprosov
from database.database import create_new_row_for_new_user, kursi
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text],
                         reply_markup=for_start_kb)
    id=message.from_user.id
    users = check_users()
    if id in users:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
        datas=vivod_dannih(message.from_user.id)
        zagruzka_dannih(id, datas)
    else:
        create_new_row_for_new_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
        if message.from_user.id not in users_db:
            users_db[message.from_user.id] = deepcopy(user_dict_template)

#начало экзамена
@router.message(F.text == 'Начать экзамен')
async def process_begin(message: Message):
    # Получаем чат ID пользователя
    chat_id = message.chat.id

    # Удаляем все сообщения с ботом в чате пользователя
    # Замените 0 на последнее сообщение с вашим ботом, если есть
    await message.bot.delete_message(chat_id, message.message_id - 1)
    book_buttons = []
    for book_name in kursi.keys():
        button = InlineKeyboardButton(text=book_name, callback_data=book_name)
        book_buttons.append([button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=book_buttons)

    await message.reply("Выберите тему:", reply_markup=keyboard)


#хендлер выбора предмета для экзамена
@router.callback_query(lambda query: query.data in kursi.keys())
async def course_callback(callback_query: CallbackQuery):
    course_name = callback_query.data

    # Создаем инлайн клавиатуру с кнопками книг
    book_buttons = []
    for book_name in kursi[course_name].keys():
        button = InlineKeyboardButton(text=book_name, callback_data=book_name)
        book_buttons.append([button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=book_buttons)
    course_name = users_db[callback_query.from_user.id]['active_course']
    await callback_query.message.edit_text(f"Выберите книгу для экзамена '{course_name}':", reply_markup=keyboard)

# Обработчик Callback-кнопок книг
@router.callback_query(lambda query: query.data in list(kursi.get(users_db[query.from_user.id]['active_course'], {}).keys()))
async def book_callback(callback_query: CallbackQuery):
    book_name = callback_query.data
    users_db[callback_query.from_user.id]['book_name']=book_name
    course_name = users_db[callback_query.from_user.id]['active_course']
    # Создаем инлайн клавиатуру с кнопками уроков
    lesson_buttons = []
    for lesson_number, lesson_id in kursi[course_name][book_name].items():
        button = InlineKeyboardButton(text=str(lesson_number), callback_data=lesson_id)
        lesson_buttons.append([button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=lesson_buttons)

    await callback_query.message.edit_text(f"Выберите номер урока для книги '{book_name}':", reply_markup=keyboard)

# Обработчик Callback-кнопок номеров уроков
@router.callback_query(lambda query: query.data in list(kursi.get(user_dict_template['active_course'], {}).get(user_dict_template['book_name'], {}).values()))
async def lesson_callback(callback_query: CallbackQuery):
    start = callback_query.data
    users_db[callback_query.from_user.id]['start']=start
    #start=str(kursi.get(user_dict_template['active_course'], {}).get(user_dict_template['book_name'], {}).get(user_dict_template['nomer_uroka']))
    #users_db[callback_query.from_user.id]['start']=start

    table=users_db[callback_query.from_user.id]['book_name']
    users_db[callback_query.from_user.id]['index']=0
    index=users_db[callback_query.from_user.id]['index']
    # Получаем текст урока по его номеру
    rows = get_ecsamen(table, start, index)  # Замените это вашей функцией получения текста урока

    await callback_query.message.edit_text(
        text=f'{LEXICON["translate"]} "{rows[1]}"',
        reply_markup=get_ecsamen_kb(rows))



#проверка ответа
@router.callback_query(lambda c: c.data in get_ecsamen(users_db[c.from_user.id]['book_name'], users_db[c.from_user.id]['start'], users_db[c.from_user.id]['index']))
async def proverka_otveta(callback: CallbackQuery):
    rows=get_ecsamen(users_db[callback.from_user.id]['book_name'], users_db[callback.from_user.id]['start'], users_db[callback.from_user.id]['index'])
    pravilno=rows[1]
    b = rows[6]
    all_rows=kolichestvo_voprosov(users_db[callback.from_user.id]['book_name'], users_db[callback.from_user.id]['start'])
    users_db[callback.from_user.id]['index'] += 1
    rows=get_ecsamen(users_db[callback.from_user.id]['book_name'], users_db[callback.from_user.id]['start'], users_db[callback.from_user.id]['index'])
    if callback.data==b:
        await callback.answer(text=LEXICON['right'],show_alert=True)
        if users_db[callback.from_user.id]['index'] < all_rows:
            await callback.message.edit_text(
                text=f'{LEXICON["translate"]} "{rows[1]}"',
                reply_markup=get_ecsamen_kb(rows))
        else:
            await callback.message.edit_text(
                text=f'{LEXICON["ending"]}',
                reply_markup=ending_ecsamen_kb
                )

    else:
        await callback.answer(text=f'{LEXICON["not_right"]} \n правильный перевод слова {pravilno} будет "{b}" \n\n',show_alert=True)
        if users_db[callback.from_user.id]['index'] < all_rows:
            await callback.message.edit_text(
                text=f'{LEXICON["translate"]} "{rows[1]}"',
                reply_markup=get_ecsamen_kb(rows)
                )
        else:
            await callback.message.edit_text(
                text=f'{LEXICON["ending"]}',
                reply_markup=ending_ecsamen_kb
                )




# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/continue"
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    rows = get_ecsamen((users_db[message.from_user.id]['index']))
    text = f'{LEXICON["translate"]}  {rows[1]}'
    await message.answer(
        text=text,
        reply_markup=get_ecsamen_kb(rows))






