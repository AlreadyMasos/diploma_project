from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


list_of_students = ['1БВТ18022', '1БВТ18034']
list_of_exer = ['отжимания', 'приседания', 'скручивания']
list_of_reps = [25, 10, 15]


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Выберите, что хотите сделать: начать тренировку (/train) или посмотреть информацию (/info).",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


class ChooseEx(StatesGroup):
    waiting_for_zachetka = State()
    waiting_for_squat = State()
    waiting_for_pushup = State()


async def train_start(message: types.Message):
    await message.answer('Выберите свой номер зачетки')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in list_of_reps:
        keyboard.add(name)
    await message.answer('Выберите упражнение:', reply_markup=keyboard)
    await ChooseEx.waiting_for_zachetka.set()


async def ex_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in list_of_students:
        await message.answer('Пожалуйста, выберите номер зачетки из списка:')
        return
    await state.update_data(chosen_zachetka=message.text.lower())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in list_of_exer:
        keyboard.add(name)
    await ChooseEx.next()
    await message.answer('Теперь выберите упражнение:', reply_markup=keyboard)


def register_handlers_ex(dp: Dispatcher):
    dp.register_message_handler()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
