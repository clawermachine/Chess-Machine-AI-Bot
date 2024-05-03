from aiogram import Router
from aiogram.types import Message
from texts.texts import TEXTS_RU

#
router = Router()

#
@router.message()
async def send_answer(message: Message):
    await message.answer(text=TEXTS_RU['other_answer'])
