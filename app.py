import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# инициализация бота и диспетчера сообщений/команд
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


# handler команды /start
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Это была команда старт')


@dp.message()
async def echo(message: types.Message):
    text = message.text.casefold()

    if text in ['привет', 'здарова', 'hi', 'hello']:
        await message.answer('И тебе привет!')
    elif text in ['пока', 'до свидания', 'bye', 'cya']:
        await message.answer('И тебе пока!')
        # await message.reply('И тебе пока!')
    else:
        await message.answer(message.text)


# бот начинает слушать сервер тг
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
