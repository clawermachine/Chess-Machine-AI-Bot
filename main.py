import asyncio
import sys
from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import Config, load_config
from config_data.db_users import allowed_users
from keyboards.set_menu import set_main_menu
from handlers import user_handlers, game_handlers, other_handlers
from middlewares.outer import Middleware_Users


#
async def main():
    logger.remove()
    logger.add('bot.log', rotation='10 MB', level='INFO')
    logger.info('Bot started')

    #
    config: Config = load_config()
    storage = MemoryStorage()
    
    #
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    dp.workflow_data.update({'allowed_users':allowed_users})

    #
    dp.startup.register(set_main_menu)
    dp.include_router(user_handlers.router)
    dp.include_router(game_handlers.router)
    dp.include_router(other_handlers.router)

    #
    dp.update.outer_middleware(Middleware_Users())

    #
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

#
asyncio.run(main())
    
