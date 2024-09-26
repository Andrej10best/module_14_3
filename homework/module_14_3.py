from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from keyboards import *
from texts import *

api = ''

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())








class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands='start')
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    result = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] - 161
    await message.answer(f'Ваша норма калорий: {result}')
    await state.finish()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('files/a.png', 'rb') as img:
        await message.answer_photo(img, f'Название: {prod_name_a} | Описание: {description_a} | Цена: {price_a}')
    with open('files/b6.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: {prod_name_b} | Описание: {description_b} | Цена: {price_b}')
    with open('files/c.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: {prod_name_c} | Описание: {description_c} | Цена: {price_c}')
    with open('files/d.png', 'rb') as img:
        await message.answer_photo(img, f'Название: {prod_name_d} | Описание: {description_d} | Цена: {price_d}')

    await message.answer(text='Выберите продукт для покупки:', reply_markup=inline_kb_product)



@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!')
    await call.answer()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)