from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from persons import PERSONS

def main_menu() -> InlineKeyboardMarkup:
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


def random_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔄 Расскажи ещё факт', callback_data='random:again')],
            [InlineKeyboardButton(text='🏠 Закончить', callback_data='random:stop')]
        ]
    )
    return keyboard


def gpt_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='❌ Закончить', callback_data='gpt:stop', style='danger')]
        ]
    )
    return keyboard


def persons_keyboard():
    buttons = [
        [InlineKeyboardButton(
            text=f'{data["emoji"]} {data["name"]}',
            callback_data=f'talk:person:{key}'
        )]
        for key, data in PERSONS.items()
    ]
    buttons.append([
        InlineKeyboardButton(text='❌ Отмена', callback_data='talk:cancel')
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def talk_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔄 Сменить собеседника', callback_data='talk:change')],
            [InlineKeyboardButton(text='🏠 Закончить', callback_data='talk:stop')]
        ]
    )


def topics_keyboard(topics: dict) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f'📚 {data["name"]}', callback_data=f'quiz:topic:{key}')]
        for key, data in topics.items()

    ]
    buttons.append(
        [InlineKeyboardButton(text='❌ Отмена', callback_data='quiz:cancel')]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def after_answer_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='➡️ Следующий вопрос', callback_data='quiz:next', style='primary')],
            [InlineKeyboardButton(text='🔄 Сменить тему', callback_data='quiz:change_topic', style='primary')],
            [InlineKeyboardButton(text='🏠 Закончить квиз', callback_data='quiz:stop', style='danger')]
        ]
    )


def news_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Закрыть сводку', callback_data='economic:stop', style='danger')]
        ]
    )