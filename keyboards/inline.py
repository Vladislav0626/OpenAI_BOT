from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🎲 Случайный факт', callback_data='menu:random', style='primary'),
                InlineKeyboardButton(text='🤖 Chat GPT', callback_data='menu:gpt', style='primary')
            ],
            [
                InlineKeyboardButton(text='💬 Диалог с личностью', callback_data='menu:talk', style='primary'),
                InlineKeyboardButton(text='❓ Квиз', callback_data='menu:quiz', style='primary')
            ],
            [
                InlineKeyboardButton(text='📈 Новости экономики', callback_data='menu:news', style='success')
            ]
        ]
    )
    return keyboard
