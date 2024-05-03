from aiogram import F, Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from loguru import logger
from texts.texts import TEXTS_RU

#
router = Router()

#
@router.message(Command(commands='start'))
async def process_start(message: Message):
    logger.info('User started chat')
    await message.answer(text=TEXTS_RU['/start'])
    

#
@router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=TEXTS_RU['/help'])


#
@router.message(Command(commands='stats'))
async def process_help(message: Message):
    await message.answer(text=TEXTS_RU['/stats'])

