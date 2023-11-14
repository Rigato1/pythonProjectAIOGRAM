from aiogram import Router
from aiogram.types import Message

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    sent_message = await message.answer(f'Это эхо! {message.text}')
    users_db[message.from_user.id]['message_id'].append(message.message_id)
    users_db[message.from_user.id]['bot_messages'].append(sent_message.message_id)