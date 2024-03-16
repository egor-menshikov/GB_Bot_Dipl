from aiogram import types, Router
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_user, orm_add_to_cart
from filters.chat_types import ChatTypeFilter
from handlers.menu_processing import get_menu_content
from keyboards.inline import MenuCallBack

user_private_rt = Router()
user_private_rt.message.filter(ChatTypeFilter(["private"]))


@user_private_rt.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name='main')

    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    user = callback.from_user
    await orm_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None,
    )
    await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
    await callback.answer("Товар добавлен в корзину.")


@user_private_rt.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    if callback_data.menu_name == 'add_to_cart':
        await add_to_cart(callback, callback_data, session)
        return

    media, reply_markup = await get_menu_content(
        session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=callback_data.page,
        product_id=callback_data.product_id,
        user_id=callback.from_user.id,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()


# Старый код, чтобы не потерять.

# from aiogram import types, Router, F
# from aiogram.filters import CommandStart, Command, or_f
# from aiogram.utils.formatting import as_list, as_marked_section, Bold
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from database.orm_query import orm_get_products
# from filters.chat_types import ChatTypeFilter
# from keyboards.reply import get_keyboard
#
# user_private_rt = Router()
# user_private_rt.message.filter(ChatTypeFilter(['private']))
#
#
# @user_private_rt.message(CommandStart())
# async def start_cmd(message: types.Message):
#     await message.answer('Это была команда старт.',
#                          reply_markup=get_keyboard(
#                              "Меню",
#                              "О магазине",
#                              "Варианты оплаты",
#                              "Варианты доставки",
#                              placeholder="Что вас интересует?",
#                              sizes=(2, 2)
#                          ))
#
#
# @user_private_rt.message(or_f(Command('menu'), F.text.casefold() == 'меню'))
# async def menu(message: types.Message, session: AsyncSession):
#     for product in await orm_get_products(session):
#         await message.answer_photo(
#             product.image,
#             caption=f'<strong>{product.name}</strong>\n{product.description}\nСтоимость: {round(product.price, 2)}',
#         )
#     await message.answer('Вот меню:')
#
#
# @user_private_rt.message(F.text.casefold() == "о магазине")
# @user_private_rt.message(Command("about"))
# async def about_cmd(message: types.Message):
#     await message.answer("О нас:")
#
#
# @user_private_rt.message(F.text.casefold() == "варианты оплаты")
# @user_private_rt.message(Command("payment"))
# async def payment_cmd(message: types.Message):
#     text = as_marked_section(
#         Bold("Варианты оплаты:"),
#         'Картой в боте',
#         'При получении',
#         'В заведении',
#         marker='✅ '
#     )
#     await message.answer(text.as_html())
#
#
# @user_private_rt.message((F.text.casefold().contains('доставк')) | (F.text.casefold() == 'варианты доставки'))
# @user_private_rt.message(Command("shipping"))
# async def menu_cmd(message: types.Message):
#     text = as_list(
#         as_marked_section(
#             Bold("Варианты доставки:"),
#             'Картой в боте',
#             'При получении',
#             'В заведении',
#             marker='✅ '
#         ),
#         as_marked_section(
#             Bold('Нельзя:'),
#             'Почта',
#             'Голуби',
#             marker='❌ '
#         ),
#         sep='\n----------------------\n')
#     await message.answer(text.as_html())
#
#
# @user_private_rt.message(F.contact)
# async def get_contact(message: types.Message):
#     await message.answer(f"номер получен")
#     await message.answer(str(message.contact))
#
#
# @user_private_rt.message(F.location)
# async def get_location(message: types.Message):
#     await message.answer(f"локация получена")
#     await message.answer(str(message.location))

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
