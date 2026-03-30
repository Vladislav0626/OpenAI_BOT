from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext  # ← добавить импорт
from keyboards.inline import main_menu
from handlers.random_fact import send_random_fact
from handlers.gpt_chat import cmd_gpt

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(f'✨ Привет, <b>{message.from_user.first_name or "друг"}</b>! ✨\n\n'
                         '🤖 Я бот с ChatGPT. Выбери, что тебя интересует:', reply_markup=main_menu(), parse_mode='html')


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '📋 <b>Команды:</b>\n\n'
        '🚀 /start - главное меню\n'
        '🎲 /random - случайный факт\n'
        '💬 /gpt - диалог с ChatGPT\n'
        '🎭 /talk - Диалог с известной личностью\n'
        '❓ /help - помощь',
        parse_mode='html'
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
async def on_menu_talk(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == 'menu:quiz')
async def on_menu_quiz(callback: CallbackQuery):
    await callback.answer()