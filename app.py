import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

from common.bot_cmds_list import private
from handlers.user_private import user_private_rt
from handlers.user_group import user_group_rt
from handlers.admin_private import admin_rt

load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message', 'edited_message']

# инициализация бота и диспетчера сообщений/команд
bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.my_admins_list = []

dp = Dispatcher()
dp.include_routers(user_private_rt, user_group_rt, admin_rt)


# бот начинает слушать сервер тг
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())
