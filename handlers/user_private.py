from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from filters.chat_types import ChatTypeFilter
from keyboards.reply import get_keyboard

user_private_rt = Router()
user_private_rt.message.filter(ChatTypeFilter(['private']))


@user_private_rt.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Это была команда старт.',
                         reply_markup=get_keyboard(
                             "Меню",
                             "О магазине",
                             "Варианты оплаты",
                             "Варианты доставки",
                             placeholder="Что вас интересует?",
                             sizes=(2, 2)
                         ))


@user_private_rt.message(or_f(Command('menu'), F.text.lower() == 'меню'))
async def menu(message: types.Message):
    await message.answer('Это будущее меню.')


@user_private_rt.message(F.text.lower() == "о магазине")
@user_private_rt.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("О нас:")


@user_private_rt.message(F.text.lower() == "варианты оплаты")
@user_private_rt.message(Command("payment"))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold("Варианты оплаты:"),
        'Картой в боте',
        'При получении',
        'В заведении',
        marker='✅ '
    )
    await message.answer(text.as_html())


@user_private_rt.message((F.text.lower().contains('доставк')) | (F.text.lower() == 'варианты доставки'))
@user_private_rt.message(Command("shipping"))
async def menu_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Варианты доставки:"),
            'Картой в боте',
            'При получении',
            'В заведении',
            marker='✅ '
        ),
        as_marked_section(
            Bold('Нельзя:'),
            'Почта',
            'Голуби',
            marker='❌ '
        ),
        sep='\n----------------------\n')
    await message.answer(text.as_html())


@user_private_rt.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f"номер получен")
    await message.answer(str(message.contact))


@user_private_rt.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f"локация получена")
    await message.answer(str(message.location))

# '|' - или
# '&' ',' - и

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
