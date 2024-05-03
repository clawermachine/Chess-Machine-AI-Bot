from aiogram import Bot
from aiogram.types import BotCommand

from texts.texts import MENU_RU

#
async def set_main_menu(bot: Bot):
    main_menu_commands = []
    for command, description in MENU_RU.items():
        main_menu_commands.append(BotCommand(command=command, description=description))

    await bot.set_my_commands(main_menu_commands)
