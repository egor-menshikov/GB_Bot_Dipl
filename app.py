import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# инициализация бота и диспетчера сообщений/команд
bot = Bot(token='7052069848:AAHy7jO5cm0Ldh2k6IYNit4bY-XTx7XBnXo')
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
    else:
        await message.answer(message.text)


# бот начинает слушать сервер тг
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
