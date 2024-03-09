from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню'),
            KeyboardButton(text='О магазине')

        ],
        [
            KeyboardButton(text='Варианты оплаты'),
            KeyboardButton(text='Варианты доставки')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню:'
)

del_kb = ReplyKeyboardRemove()

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text='Меню'),
    KeyboardButton(text='О магазине'),
    KeyboardButton(text='Варианты оплаты'),
    KeyboardButton(text='Варианты доставки')
)
start_kb2.adjust(2, 2)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(
    KeyboardButton(text='Оставить отзыв')
)

test_kb = ReplyKeyboardBuilder()
test_kb.add(
    KeyboardButton(text='Создать опрос', request_poll=KeyboardButtonPollType()),
    KeyboardButton(text='Отправить номер', request_contact=True),
    KeyboardButton(text='Отправить локацию', request_location=True)
)
test_kb.adjust(1, 1, 1)
