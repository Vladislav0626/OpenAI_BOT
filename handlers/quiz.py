import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from aiogram.types import Message, FSInputFile, CallbackQuery
from services.openai_service import ask_gpt
from states.state import QuizStates
from keyboards.inline import topics_keyboard, after_answer_keyboard, main_menu
from utils.quiz_generate import send_next_question, check_answer
from data.topics import TOPICS

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command('quiz'))
async def cmd_quiz(message: Message, state: FSMContext):
    await state.set_state(QuizStates.choosing_topics)

    try:
        photo = FSInputFile('images/quiz.png')
        await message.answer_photo(
            photo=photo,
            caption='<b>❓ Квиз с ChatGPT</b>\n\nВыбери тему — и погнали!',
            reply_markup=topics_keyboard(TOPICS),
            parse_mode='html'
        )
    except Exception:
        await message.answer(
            '<b>❓ Квиз с ChatGPT</b>\n\nВыбери тему — и погнали!',
            reply_markup=topics_keyboard(TOPICS),
            parse_mode='html'
        )


@router.callback_query(QuizStates.choosing_topics, F.data.startswith('quiz:topic'))
async def on_topic_choosing(callback: CallbackQuery, state: FSMContext):
    topic_key = callback.data.split(':')[-1]

    if topic_key not in TOPICS:
        await callback.answer('Это неизвестная тема')
        return

    topic = TOPICS[topic_key]

    await state.update_data(
        topic_key=topic_key,
        score=0,
        total=0,
        current_question=''
    )
    await state.set_state(QuizStates.answering)

    await callback.answer(f'Тема {topic["name"]}')

    await callback.message.edit_caption(
        caption=f'{topic["name"]} — отличный выбор!\n\nГенерирую вопрос...'
    )

    await send_next_question(callback.message, state, topic_key)


@router.message(QuizStates.answering, F.text)
async def cmd_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    current_question = data.get('current_question', '')
    score = data.get('score', 0)
    total = data.get('total', 0)

    if not current_question:
        await message.answer('Что-то пошло не так. Начни заново /quiz')
        await state.clear()
        return

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    is_correct, explanation = await check_answer(current_question, message.text)

    new_total = total + 1
    new_score = score + (1 if is_correct else 0)

    await state.update_data(score=new_score, total=new_total, current_question='')

    result_header = '✅ Верно!' if is_correct else '❌ Неверно!'

    await message.answer(
        f'{result_header}\n\n'
        f'{explanation}\n\n'
        f'📊 Счёт: <b>{new_score}/{new_total}</b>',
        reply_markup=after_answer_keyboard(),
        parse_mode='html'
    )


@router.callback_query(F.data == 'quiz:next')
async def on_quiz_next(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    topic_key = data.get('topic_key')

    if not topic_key:
        await callback.message.answer('Ошибка. Начни квиз заново /quiz')
        await state.clear()
        return

    await send_next_question(callback.message, state, topic_key)


@router.callback_query(F.data == 'quiz:change_topic')
async def on_quiz_change_topic(callback: CallbackQuery, state: FSMContext):
    await state.set_state(QuizStates.choosing_topics)
    await state.update_data(score=0, total=0, current_question='')

    await callback.answer()
    await callback.message.delete()  # удаляем старое сообщение

    await callback.message.answer(
        '🎯 Выбери новую тему:',
        reply_markup=topics_keyboard(TOPICS),
        parse_mode='html'
    )


@router.callback_query(F.data == 'quiz:stop')
async def on_quiz_stop(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    score = data.get('score', 0)
    total = data.get('total', 0)

    await state.clear()
    await callback.answer()
    await callback.message.delete()

    if total == 0:
        verdict = '❌ Ты не ответил ни на один вопрос!'
    elif score == total:
        verdict = '🏆 Идеальный результат!'
    elif score / total >= 0.75:
        verdict = '👍 Отличный результат!'
    elif score / total >= 0.4:
        verdict = '📚 Неплохо, но есть куда расти!'
    else:
        verdict = '📖 Стоит подтянуть знания!'

    await callback.message.answer(
        f'<b>📊 Квиз завершён!</b>\n\n'
        f'✅ Правильных ответов: <b>{score} из {total}</b>\n\n'
        f'{verdict}',
        parse_mode='html'
    )


@router.callback_query(F.data == 'quiz:cancel')
async def on_quiz_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('🏠 Главное меню', reply_markup=main_menu())

    try:
        await callback.message.edit_caption(caption='❌ Квиз отменён')
    except Exception:
        await callback.message.edit_text('❌ Квиз отменён')