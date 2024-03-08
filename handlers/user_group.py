from aiogram import types, Router, F
from string import punctuation
from aiogram.filters import CommandStart, Command, or_f

user_group_rt = Router()
user_group_rt.message.filter()

RESTRICTED_WORDS = {'хуй', 'пизда'}


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_rt.edited_message()
@user_group_rt.message()
async def profanity_filter(message: types.Message):
    if RESTRICTED_WORDS.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.username} ай как нехорошо.')
        await message.delete()
        # await message.chat.ban(message.from_user.id)
