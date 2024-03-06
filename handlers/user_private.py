from aiogram import types, Router
from aiogram.filters import CommandStart, Command

user_private_rt = Router()


@user_private_rt.message(CommandStart())
async def start_cmd_egor_leon(message: types.Message):
    await message.answer('Это была команда старт.')


@user_private_rt.message(Command('menu'))
async def menu_egor_leon(message: types.Message):
    await message.answer('Это будущее меню.')


@user_private_rt.message(Command('test_command_1'))
async def menu_test_1_egor_leon(message: types.Message):
    await message.answer('Это тестовая команда 1.')


@user_private_rt.message(Command('test_command_2'))
async def menu_test_2_egor_leon(message: types.Message):
    await message.answer('Это тестовая команда 2.')


@user_private_rt.message()
async def echo_egor_leon(message: types.Message):
    text = message.text.casefold()

    if text in ['привет', 'здарова', 'hi', 'hello']:
        await message.answer('И тебе привет!')
    elif text in ['пока', 'до свидания', 'bye', 'cya']:
        await message.answer('И тебе пока!')
    else:
        await message.answer(message.text)
