import os

from aiogram import types, Router
from string import punctuation
from dotenv import find_dotenv, load_dotenv

from filters.chat_types import ChatTypeFilter

load_dotenv(find_dotenv())

PROFANITY = set(os.getenv('PROFANITY').split(','))

user_group_rt = Router()
user_group_rt.message.filter(ChatTypeFilter(['group', 'supergroup']))


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_rt.edited_message()
@user_group_rt.message()
async def profanity_filter(message: types.Message):
    if PROFANITY.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.username} ай как нехорошо.')
        await message.delete()
        # await message.chat.ban(message.from_user.id)
