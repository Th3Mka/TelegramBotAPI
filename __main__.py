from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Токен бота
BOT_TOKEN = '7019020416:AAEzoV1cJIzk78yZMOp3bo86IwJ6ZwLBww8'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализируем билдер
kb_builder = ReplyKeyboardBuilder()

# Создаем кнопки
survey_btn = KeyboardButton(text='Пройти опрос')
quiz_btn = KeyboardButton(text='Пройти викторину')

# Добавляем кнопки в билдер
kb_builder.row(survey_btn, quiz_btn, width=2)

# Создаем объект клавиатуры
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)

# Опросные вопросы
survey_questions = [
    "Из какого вы города ?",
    "Сколько вам лет?",
    "Какой ваш любимый спорт?"
]

# Викторинные вопросы, варианты ответов и правильные ответы
quiz_questions = [
    ("Какой язык является самым распространенным в мире?", ["Испанский", "Английский", "Китайский"], "Китайский"),
    ("Какой морской млекопитающий известен своим 'пением'?", ["Дельфин", "Кит", "Тюлень"], "Кит"),
    ("Какое животное считается самым быстрым на земле?", ["Гепард", "Сокол", "Слон"], "Гепард"),
    ("Какой город является столицей Японии?", ["Осака", "Токио", "Киото"], "Токио"),
]

# Переменные для хранения состояния пользователя
user_data = {}

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Выберите, что хотите сделать:", reply_markup=keyboard)

# Обработчик кнопки "Пройти опрос"
@dp.message(lambda message: message.text == 'Пройти опрос')
async def start_survey(message: Message):
    user_data[message.from_user.id] = {"survey_step": 0, "survey_answers": []}
    await ask_survey_question(message)

async def ask_survey_question(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["survey_step"]
    question = survey_questions[step]
    await message.answer(question, reply_markup=types.ReplyKeyboardRemove())  # Убираем клавиатуру для ввода текста

@dp.message(lambda message: message.from_user.id in user_data and "survey_step" in user_data[message.from_user.id])
async def handle_survey_answer(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["survey_step"]
    user_data[user_id]["survey_answers"].append(message.text)

    # Если есть еще вопросы
    if step + 1 < len(survey_questions):
        user_data[user_id]["survey_step"] += 1
        await ask_survey_question(message)
    else:
        # Выводим результаты опроса
        results = "\n".join(f"{q}: {a}" for q, a in zip(survey_questions, user_data[user_id]["survey_answers"]))
        await message.answer(f"Спасибо за участие в опросе!\nВаши ответы:\n{results}", reply_markup=keyboard)
        del user_data[user_id]  # Очищаем данные пользователя после завершения опроса

# Обработчик кнопки "Пройти викторину"
@dp.message(lambda message: message.text == 'Пройти викторину')
async def start_quiz(message: Message):
    user_data[message.from_user.id] = {"quiz_step": 0, "correct_answers": 0}
    await ask_quiz_question(message)

async def ask_quiz_question(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["quiz_step"]
    question, options, _ = quiz_questions[step]
    kb_builder = ReplyKeyboardBuilder()
    for option in options:
        kb_builder.button(text=option)
    keyboard = kb_builder.as_markup(resize_keyboard=True)
    await message.answer(question, reply_markup=keyboard)

@dp.message(lambda message: message.text in [option for q, o, a in quiz_questions for option in o])
async def handle_quiz_answer(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["quiz_step"]
    _, _, correct_answer = quiz_questions[step]

    if message.text == correct_answer:
        user_data[user_id]["correct_answers"] += 1
        await message.answer("Правильно!")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {correct_answer}")

    # Если есть еще вопросы
    if step + 1 < len(quiz_questions):
        user_data[user_id]["quiz_step"] += 1
        await ask_quiz_question(message)
    else:
        # Выводим результаты викторины
        total_questions = len(quiz_questions)
        correct_answers = user_data[user_id]["correct_answers"]
        await message.answer(f"Викторина окончена! Вы ответили правильно на {correct_answers} из {total_questions} вопросов.", reply_markup=keyboard)
        del user_data[user_id]  # Очищаем данные пользователя после завершения викторины


# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)
