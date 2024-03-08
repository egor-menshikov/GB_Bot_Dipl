from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f

user_private_rt = Router()
user_private_rt.message.filter()


@user_private_rt.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Это была команда старт.')


@user_private_rt.message(or_f(Command('menu'), F.text.lower() == 'меню'))
async def menu(message: types.Message):
    await message.answer('Это будущее меню.')


@user_private_rt.message(Command('test_command_1'))
async def menu_test_1(message: types.Message):
    await message.answer('Это тестовая команда 1.')


@user_private_rt.message(Command('test_command_2'))
async def menu_test_2(message: types.Message):
    await message.answer('Это тестовая команда 2.')


# '|' - или
# '&' ',' - и
@user_private_rt.message(F.text, F.text.lower() == 'варианты')
async def magic_filter_test(message: types.Message):
    await message.answer('Это магический фильтр.')

# @user_private_rt.message()
# async def echo(message: types.Message):
#     text = message.text.casefold()
#
#     if text in ['привет', 'здарова', 'hi', 'hello']:
#         await message.answer('И тебе привет!')
#     elif text in ['пока', 'до свидания', 'bye', 'cya']:
#         await message.answer('И тебе пока!')
#     else:
#         await magic_filter_test(message)
