from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from services.openai_service import ask_gpt
from data.topics import TOPICS


async def generate_answer(topic_key: str) -> str:
    """Генерирует вопрос по теме"""
    topic = TOPICS[topic_key]

    prompt = (
        f'Ты ведущий квиза. Задай один интересный, но не сильно сложный вопрос по теме: {topic["prompt_name"]}. '
        'Вопрос должен иметь чёткий и однозначный ответ. '
        'Напиши только сам вопрос, без нумерации и ответа.'
    )

    return await ask_gpt(user_message=prompt)


async def check_answer(question: str, user_answer: str) -> tuple[bool, str]:
    """Отправляет вопрос и ответ в GPT для проверки"""
    prompt = (
        f"Вопрос квиза: {question}\n"
        f"Ответ пользователя: {user_answer}\n\n"
        "Оцени правильность ответа. Отвечай строго в следующем формате:\n"
        "Первая строка: только слово ВЕРНО или НЕВЕРНО.\n"
        "Вторая строка и далее: краткое объяснение (1-2 предложения).\n"
        "Если ответ неверный, укажи правильный ответ."
    )

    response = await ask_gpt(user_message=prompt)

    lines = response.strip().split('\n')
    first_line = lines[0].strip().upper()

    is_correct = first_line.startswith('ВЕРНО')

    explanation = '\n'.join(lines[1:]).strip()

    if not explanation:
        explanation = 'Засчитано' if is_correct else 'Неправильно'

    return is_correct, explanation


async def send_next_question(message: Message, state: FSMContext, topic_key: str):
    """Генерирует вопрос, отправляет пользователю и сохраняет в FSM"""
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    question = await generate_answer(topic_key)

    await state.update_data(current_question=question)
    data = await state.get_data()
    score = data.get('score', 0)
    total = data.get('total', 0)
    topic_name = TOPICS[topic_key]['name']

    await message.answer(
        f'Счёт <b>{score}/{total} | Тема: {topic_name}</b>\n\n'
        f'<b>Вопрос</b>\n{question}',
        parse_mode='html'
    )