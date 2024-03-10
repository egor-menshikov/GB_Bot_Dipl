import os

from aiogram import types, Router, Bot
from string import punctuation

from aiogram.filters import Command
from dotenv import find_dotenv, load_dotenv

from filters.chat_types import ChatTypeFilter

load_dotenv(find_dotenv())

PROFANITY = set(os.getenv('PROFANITY').split(','))

user_group_rt = Router()
user_group_rt.message.filter(ChatTypeFilter(['group', 'supergroup']))
user_group_rt.edited_message.filter(ChatTypeFilter(['group', 'supergroup']))


@user_group_rt.message(Command('admin'))
async def get_admins(message: types.Message, bot: Bot):
    admins_list = await bot.get_chat_administrators(message.chat.id)
    # Посмотрим имена админов и их id
    # for item in admins_list:
    #     await message.answer(item.user.username + ' | ' + str(item.user.id))
    bot.my_admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    if message.from_user.id in admins_list:
        await message.delete()


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_rt.edited_message()
@user_group_rt.message()
async def profanity_filter(message: types.Message):
    if PROFANITY.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.username} ай как нехорошо.')
        await message.delete()
        # await message.chat.ban(message.from_user.id)
