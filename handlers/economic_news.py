import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.enums import ChatAction
from pyexpat.errors import messages
from services.openai_service import ask_gpt
from keyboards.inline import random_keyboard, main_menu, news_keyboard


now_time = datetime.now()


router = Router()
logger = logging.getLogger(__name__)

NEWS_PROMPT = (
    f"Предоставь краткую сводку экономических новостей на сегодня {now_time}."
    "Используй следующий порядок тем: глобальная экономика, фондовые рынки, криптовалюты, остальные важные события. "
    "Текст должен быть не длиннее 1000 символов. Это обязательное условие"
    "Не используй форматирование (жирный шрифт, списки, заголовки). Пиши сплошным текстом, но с использований абзацев для удобства чтения. "
    "Оставляй только суть: ключевые события, цифры и их влияние. Игнорируй второстепенные детали и прогнозы. "
    "Дай факты без воды, лишних слов и оценок. "
    "В конце обязательно укажи дату выпуска сводки в формате ДД.ММ.ГГГГ."
)


async def send_economic_news(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    news_prompt = await ask_gpt(user_message=NEWS_PROMPT)

    try:
        photo = FSInputFile('images/economic.png')
        await message.answer_photo(
            photo=photo,
            caption=f'<b>📈 Новости экономики</b>\n\n{news_prompt}',
            reply_markup=news_keyboard(),
            parse_mode='html'
        )
    except Exception:
        logger.exception('Не удалось отправить фото')
        await message.answer(
            f'<b>📈 Новости экономики</b>\n\n{news_prompt}',
            reply_markup=news_keyboard(),
            parse_mode='html'
        )


@router.message(Command('news'))
async def cmd_news(message: Message):
    await send_economic_news(message)


@router.callback_query(F.data == 'economic:stop')
async def cmd_random_stop(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('🏠 Выбери пункт', reply_markup=main_menu())