from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db, check_users, vivod_dannih
from keyboards.ecsamen_kb import get_ecsamen_kb, ending_ecsamen_kb
from keyboards.knopki_urokov import for_start_kb
from lexicon.lexicon import LEXICON
from services.services import get_ecsamen, zagruzka_dannih, kolichestvo_voprosov
from database.database import create_new_row_for_new_user, kursi, add_completed_topic, sbros_galochek
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import html
router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    sent_message = await message.answer(LEXICON[message.text], reply_markup=for_start_kb)
    id=message.from_user.id
    if message.from_user.id not in users_db:
        users_db[id] = copy.deepcopy(user_dict_template)
    users = check_users()
    if id not in users:
        create_new_row_for_new_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)



    # строка для добавления айди бота в список чтобы очищать сообщения перед экзаменом
    users_db[message.from_user.id]['message_id'].append(message.message_id)
    users_db[message.from_user.id]['bot_messages'].append(sent_message.message_id)





#начало экзамена
@router.message(F.text == 'Начать экзамен')
async def process_begin(message: Message):
    print(users_db)
    users_db[message.from_user.id]['message_id'].append(message.message_id)
    # Получаем чат ID пользователя
    chat_id = message.chat.id

    #здесь мы очищаем все сообщения из чата
    messages_ids = users_db[message.from_user.id]['message_id']
    bot_messages = users_db[message.from_user.id]['bot_messages']
    for message_id in messages_ids:
        await message.bot.delete_message(chat_id, message_id)
    for message_id in bot_messages:
        await message.bot.delete_message(chat_id, message_id)
    book_buttons = []
    users_db[message.from_user.id]['message_id']=[]
    users_db[message.from_user.id]['bot_messages']=[]
    for book_name in kursi.keys():
        button = InlineKeyboardButton(text=book_name, callback_data=book_name)
        book_buttons.append([button])
    datas = vivod_dannih(message.from_user.id)
    zagruzka_dannih(message.from_user.id, datas)
    keyboard = InlineKeyboardMarkup(inline_keyboard=book_buttons)

    await message.answer("Выберите тему:", reply_markup=keyboard)




#кнопка перезапуска когда кончаются слова
@router.callback_query(F.data=='restart')
async def restart_func(callback_query: CallbackQuery):
    start = users_db[callback_query.from_user.id]['start']
    table = users_db[callback_query.from_user.id]['book_name']
    users_db[callback_query.from_user.id]['index'] = 0
    index = users_db[callback_query.from_user.id]['index']
    # Получаем текст урока по его номеру
    rows = get_ecsamen(table, start, index)  # Замените это вашей функцией получения текста урока

    await callback_query.message.edit_text(
        text=f'{LEXICON["translate"]} "{rows[1]}"',
        reply_markup=get_ecsamen_kb(rows))




#кнопка выбора другой темы просто перекидывает в начало инлайн клавиатуры
@router.callback_query(F.data=='New_theme')
async def new_theme_func(callback_query: CallbackQuery):
    book_buttons=[]

    datas = vivod_dannih(callback_query.from_user.id)
    zagruzka_dannih(callback_query.from_user.id, datas)
    for book_name in kursi.keys():
        button = InlineKeyboardButton(text=book_name, callback_data=book_name)
        book_buttons.append([button])
    users_db[callback_query.from_user.id]['start'] = ''
    keyboard = InlineKeyboardMarkup(inline_keyboard=book_buttons)

    await callback_query.message.edit_text("Выберите тему:", reply_markup=keyboard)



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
    users_db[callback_query.from_user.id]['start']=[]
    lesson_buttons = []
    for lesson_number, lesson_id in kursi[course_name][book_name].items():
        if lesson_id in users_db[callback_query.from_user.id]['Мединский_курс_том_1']:
            button = InlineKeyboardButton(text=f'{lesson_number}✅', callback_data=lesson_id)
        else:
            button = InlineKeyboardButton(text=str(lesson_number), callback_data=lesson_id)
        lesson_buttons.append([button])
    sbros = InlineKeyboardButton(text='Сбросить галочки', callback_data='sbros')
    lesson_buttons.append([sbros])

    keyboard = InlineKeyboardMarkup(inline_keyboard=lesson_buttons)

    await callback_query.message.edit_text(f"Выберите номер урока для книги '{book_name}':", reply_markup=keyboard)



#сброс галочек
@router.callback_query(F.data=='sbros')
async def sbros(callback_query: CallbackQuery):
    sbros_galochek(callback_query.from_user.id, users_db[callback_query.from_user.id]['book_name'])
    users_db[callback_query.from_user.id][users_db[callback_query.from_user.id]['book_name']]=''
    book_buttons = []
    for book_name in kursi.keys():
        button = InlineKeyboardButton(text=book_name, callback_data=book_name)
        book_buttons.append([button])
    users_db[callback_query.from_user.id]['start'] = ''
    keyboard = InlineKeyboardMarkup(inline_keyboard=book_buttons)
    await callback_query.message.edit_text("Выберите тему:", reply_markup=keyboard)




# Обработчик Callback-кнопок номеров уроков
@router.callback_query(lambda query: query.data in list(kursi.get(user_dict_template['active_course'], {}).get(user_dict_template['book_name'], {}).values()))
async def lesson_callback(callback_query: CallbackQuery):
    users_db[callback_query.from_user.id]['start']=callback_query.data
    table=users_db[callback_query.from_user.id]['book_name']
    users_db[callback_query.from_user.id]['index']=0
    index=users_db[callback_query.from_user.id]['index']
    users_db[callback_query.from_user.id]['sahihs'] = 0
    rows = get_ecsamen(users_db[callback_query.from_user.id]['book_name'], callback_query.data,
                       users_db[callback_query.from_user.id]['index'])
    kol_vo = kolichestvo_voprosov(users_db[callback_query.from_user.id]['book_name'],
                                  users_db[callback_query.from_user.id]['start'])
    text = f'{index}/{kol_vo} \n{LEXICON["translate"]} <b>{rows[1]}</b>'
    # Получаем текст урока по его номеру

    await callback_query.message.edit_text(
        text=text,
        reply_markup=get_ecsamen_kb(rows, table))



#проверка ответа
@router.callback_query(lambda c: c.data in get_ecsamen(users_db[c.from_user.id]['book_name'], users_db[c.from_user.id]['start'], users_db[c.from_user.id]['index']))
async def proverka_otveta(callback: CallbackQuery):
    rows=get_ecsamen(users_db[callback.from_user.id]['book_name'], users_db[callback.from_user.id]['start'], users_db[callback.from_user.id]['index'])
    pravilno=rows[1]
    users_db[callback.from_user.id]['sahihs']
    b = rows[6]
    table = users_db[callback.from_user.id]['book_name']
    kol_vo=kolichestvo_voprosov(users_db[callback.from_user.id]['book_name'], users_db[callback.from_user.id]['start'])
    users_db[callback.from_user.id]['index'] += 1
    index = users_db[callback.from_user.id]['index']
    rows=get_ecsamen(users_db[callback.from_user.id]['book_name'], users_db[callback.from_user.id]['start'], users_db[callback.from_user.id]['index'])
    if callback.data==b:
        await callback.answer(text=LEXICON['right'])
        users_db[callback.from_user.id]['sahihs']+=1
        if users_db[callback.from_user.id]['index'] < kol_vo:
            text = f'{index}/{kol_vo} \n{LEXICON["translate"]} <b>{rows[1]}</b>'
            markup = get_ecsamen_kb(rows, table)
            await callback.message.edit_text(text=text, reply_markup=markup, parse_mode="HTML")
        elif users_db[callback.from_user.id]['index'] == kol_vo:
            if users_db[callback.from_user.id]['sahihs'] == kol_vo:
                nomera_urokov=str(users_db[callback.from_user.id][users_db[callback.from_user.id]['book_name']])
                if users_db[callback.from_user.id]['start'] not in nomera_urokov:
                    add_completed_topic(callback.from_user.id, users_db[callback.from_user.id]['book_name'],users_db[callback.from_user.id]['start'])
                    users_db[callback.from_user.id][users_db[callback.from_user.id]['book_name']] += users_db[callback.from_user.id]['start']
                    await callback.message.edit_text(
                        text=f'{LEXICON["ending"]}',
                        reply_markup=ending_ecsamen_kb
                    )
                else:
                    await callback.message.edit_text(
                    text=f'{LEXICON["ending"]}',
                    reply_markup=ending_ecsamen_kb
                    )
            else:
                await callback.message.edit_text(
                    text=f'{LEXICON["ending"]}',
                    reply_markup=ending_ecsamen_kb
                )

    else:
        await callback.answer(text=f'{LEXICON["not_right"]} \n правильный перевод слова {pravilno} будет "{b}" \n\n',show_alert=True)
        if users_db[callback.from_user.id]['index'] < kol_vo:
            await callback.message.edit_text(
                text=f'{LEXICON["translate"]} "{rows[1]}"',
                reply_markup=get_ecsamen_kb(rows,table)
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
    sent_message = await message.answer(LEXICON[message.text])
    users_db[message.from_user.id]['bot_messages'].append(sent_message.message_id)
    users_db[message.from_user.id]['message_id'].append(message.message_id)



# Этот хэндлер будет срабатывать на команду "/continue"
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    rows = get_ecsamen((users_db[message.from_user.id]['index']))
    text = f'{LEXICON["translate"]}  {rows[1]}'
    await message.answer(
        text=text,
        reply_markup=get_ecsamen_kb(rows))
    users_db[message.from_user.id]['message_id'].append(message.message_id)






