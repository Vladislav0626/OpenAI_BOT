from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline import main_menu
from handlers.random_fact import send_random_fact
from handlers.gpt_chat import cmd_gpt

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        f'✨ Привет, <b>{message.from_user.first_name or "друг"}</b>! ✨\n\n'
        '🤖 Я бот с ChatGPT. Выбери, что тебя интересует:',
        reply_markup=main_menu(),
        parse_mode='html'
    )


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '📋 <b>Команды:</b>\n\n'
        '🚀 /start - главное меню\n'
        '🎲 /random - случайный факт\n'
        '💬 /gpt - диалог с ChatGPT\n'
        '🎭 /talk - диалог с личностью\n'
        '❓ /quiz - квиз\n'
        '❓ /help - помощь',
        parse_mode='html'
    )

@router.message(Command('git'))
async def cmd_git(message: Message):
    await message.answer(
        'Ссылка на репозиторий GitHub: https://github.com/Vladislav0626/OpenAI_BOT'
        'Нажми /start чтобы продолжить использовать бота!'
    )


@router.callback_query(F.data == 'menu:random')
async def on_menu_random(callback: CallbackQuery):
    await callback.answer()
    await send_random_fact(callback.message)


@router.callback_query(F.data == 'menu:gpt')
async def on_menu_gpt(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await cmd_gpt(callback.message, state)


@router.callback_query(F.data == 'menu:talk')
async def on_menu_talk(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    from handlers.talk import cmd_talk
    await cmd_talk(callback.message, state)


@router.callback_query(F.data == 'menu:quiz')
async def on_menu_quiz(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    from handlers.quiz import cmd_quiz
    await cmd_quiz(callback.message, state)


@router.callback_query(F.data == 'menu:news')
async def on_menu_news(callback: CallbackQuery):
    await callback.answer()
    from handlers.economic_news import cmd_news
    await cmd_news(callback.message)

