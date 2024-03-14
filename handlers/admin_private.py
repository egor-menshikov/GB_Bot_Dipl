from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_product, orm_get_products, orm_delete_product
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.inline import get_callback_btns
from keyboards.reply import get_keyboard

admin_rt = Router()
admin_rt.message.filter(ChatTypeFilter(['private']), IsAdmin())

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2,),
)


@admin_rt.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_rt.message(F.text.casefold() == "ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f'<strong>{product.name}</strong>\n{product.description}\nСтоимость: {round(product.price, 2)}',
            reply_markup=get_callback_btns(btns={
                'Удалить': f'delete_{product.id}',
                'Изменить': f'change_{product.id}'
            })
        )
    await message.answer("ОК, вот список товаров")


@admin_rt.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split('_')[-1]
    await orm_delete_product(session, int(product_id))
    await callback.answer('Товар удален')
    await callback.message.answer('Товар удален!')


# Код ниже для машины состояний (FSM)
class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    texts = {
        'AddProduct:name': 'Введите название заново:',
        'AddProduct:description': 'Введите описание заново:',
        'AddProduct:price': 'Введите стоимость заново:',
        'AddProduct:image': 'Этот стейт последний, поэтому...',
    }


@admin_rt.message(StateFilter(None), F.text.casefold() == "добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_rt.message(StateFilter('*'), Command("отмена"))
@admin_rt.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_rt.message(StateFilter('*'), Command("назад"))
@admin_rt.message(StateFilter('*'), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer('Предидущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}")
            return
        previous = step


# Название
@admin_rt.message(StateFilter(AddProduct.name), F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)


@admin_rt.message(StateFilter(AddProduct.name))
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Введите название товара корректно")


# Описание
@admin_rt.message(StateFilter(AddProduct.description), F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара")
    await state.set_state(AddProduct.price)


@admin_rt.message(StateFilter(AddProduct.description))
async def add_description(message: types.Message, state: FSMContext):
    await message.answer("Введите описание товара корректно")


# Стоимость
@admin_rt.message(StateFilter(AddProduct.price), F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)


@admin_rt.message(StateFilter(AddProduct.price))
async def add_price(message: types.Message, state: FSMContext):
    await message.answer("Введите стоимость товара корректно")


# Изображение
@admin_rt.message(StateFilter(AddProduct.image), F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()

    try:
        await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
        await orm_add_product(session, data)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет",
            reply_markup=ADMIN_KB
        )
        await state.clear()


@admin_rt.message(StateFilter(AddProduct.image), F.photo)
async def add_image(message: types.Message, state: FSMContext):
    await message.answer("Загрузите изображение товара корректно", reply_markup=ADMIN_KB)
