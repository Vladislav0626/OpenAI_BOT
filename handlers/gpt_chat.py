import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from services.openai_service import ask_gpt
from keyboards.inline import gpt_keyboard, main_menu
from states.state import GptStates

router = Router()
logger = logging.getLogger(__name__)

GPT_SYSTEM_PROMPT = (
    "Ты — дружелюбный и полезный ассистент. Не будь занудой. "
    "Отвечай на том же языке, на котором написан запрос. "
    "Отвечай по делу, без лишних вступлений."
)

@router.message(Command('gpt'))
async def cmd_gpt(message: Message, state: FSMContext):
    await state.set_state(GptStates.chatting)
    await state.update_data(history=[])

    try:
        photo = FSInputFile('images/gpt.png')
        await message.answer_photo(
            photo=photo,
            caption='<b>🤖 Режим ChatGPT</b>\n\nНапиши любой вопрос — я отвечу.\n❌ Нажми Закончить, чтобы выйти.',
            reply_markup=gpt_keyboard(),
            parse_mode='html'
        )
    except Exception:
        await message.answer(
            '<b>🤖 Режим ChatGPT</b>\n\nНапиши любой вопрос — я отвечу.\n❌ Нажми Закончить, чтобы выйти.',
            reply_markup=gpt_keyboard(),
            parse_mode='html'
        )

@router.message(GptStates.chatting, F.text)
async def cmd_gpt_message(message: Message, state: FSMContext):
    data = await state.get_data()
    history = data.get('history', [])

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    history.append({'role': 'user', 'content': message.text})

    response = await ask_gpt(
        user_message=message.text,
        system_prompt=GPT_SYSTEM_PROMPT,
        history=history[:-1]
    )

    history.append({'role': 'assistant', 'content': response})

    if len(history) > 20:
        history = history[-20:]

    await state.update_data(history=history)
    await message.answer(response, reply_markup=gpt_keyboard())

@router.callback_query(F.data == 'gpt:stop')
async def on_gpt_stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Выхожу из режима ChatGPT')
    await callback.message.delete()
    await callback.message.answer('✅ Режим ChatGPT завершён', reply_markup=main_menu())