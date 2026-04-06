import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from services.openai_service import ask_gpt
from keyboards.inline import main_menu, persons_keyboard, talk_keyboard
from states.state import TalkStates
from persons import PERSONS

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command('talk'))
async def cmd_talk(message: Message, state: FSMContext):
    await state.set_state(TalkStates.choosing_person)

    try:
        photo = FSInputFile('images/talk.png')
        await message.answer_photo(
            photo=photo,
            caption='<b>🎭 Диалог с известной личностью</b>\n\nВыбери, с кем хочешь поговорить:',
            reply_markup=persons_keyboard(),
            parse_mode='html'
        )
    except Exception:
        await message.answer(
            '<b>🎭 Диалог с известной личностью</b>\n\nВыбери, с кем хочешь поговорить:',
            reply_markup=persons_keyboard(),
            parse_mode='html'
        )

@router.callback_query(TalkStates.choosing_person, F.data.startswith('talk:person:'))
async def on_person_choosen(callback: CallbackQuery, state: FSMContext):
    person_key = callback.data.split(':')[-1]

    if person_key not in PERSONS:
        await callback.answer('Неизвестная личность')
        return

    person = PERSONS[person_key]

    await state.update_data(person_key=person_key, history=[])
    await state.set_state(TalkStates.chatting)

    await callback.answer(f'Начинаем разговор с {person["name"]}')

    await callback.message.edit_caption(
        caption=f'{person["emoji"]} <b>Вы разговариваете с {person["name"]}</b>\n\nНапиши что-нибудь — получишь ответ в его стиле',
        reply_markup=talk_keyboard(),
        parse_mode='html'
    )

@router.message(TalkStates.chatting, F.text)
async def talk_message(message: Message, state: FSMContext):
    data = await state.get_data()
    person_key = data.get('person_key')
    history = data.get('history', [])

    if person_key not in PERSONS:
        await message.answer('Что-то пошло не так! Начни заново /talk')
        await state.clear()
        return

    person = PERSONS[person_key]

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    history.append({'role': 'user', 'content': message.text})

    response = await ask_gpt(
        user_message=message.text,
        system_prompt=person['prompt'],
        history=history[:-1]
    )

    history.append({'role': 'assistant', 'content': response})

    if len(history) > 20:
        history = history[-20:]

    await state.update_data(history=history)
    await message.answer(f'{person["emoji"]} <b>{person["name"]}</b>\n\n{response}')

@router.callback_query(F.data == 'talk:change')
async def change_person(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TalkStates.choosing_person)
    await callback.answer('Выбирай нового собеседника')
    await callback.message.delete()
    await callback.message.answer(
        '🎭 Выбери, с кем хочешь поговорить:',
        reply_markup=persons_keyboard(),
        parse_mode='html'
    )

@router.callback_query(F.data == 'talk:stop')
async def stop_talk(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Выхожу из диалога')
    await callback.message.delete()
    await callback.message.answer('🏠 Главное меню', reply_markup=main_menu())

@router.callback_query(F.data == 'talk:cancel')
async def cancel_talk(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Отмена')
    await callback.message.delete()
    await callback.message.answer('🏠 Главное меню', reply_markup=main_menu())