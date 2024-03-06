import asyncio
import os

from aiogram import Bot, Dispatcher, types

from dotenv import find_dotenv, load_dotenv
from handlers.user_private import user_private_rt

load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message', 'edited_message']

# инициализация бота и диспетчера сообщений/команд
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_routers(user_private_rt)


# бот начинает слушать сервер тг
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())
