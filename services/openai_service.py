from openai import AsyncOpenAI
from config import TOKEN_GPT_AI
import logging
import asyncio

from pygments.console import ansiformat

cliet = AsyncOpenAI(api_key=TOKEN_GPT_AI)
MODEL = 'gpt-4o-mini'


logger = logging.getLogger(__name__)


async def ask_gpt(
        user_message = str,
        system_promt: str = 'Ты полезный ассистент. Отвечай кратко и по делу.',
        history: list = None
) -> str:

    try:
        messages = [{'role': 'system', 'content': system_promt}]

        if history:
            messages.append(history)
        messages.append({'role': 'user', 'content': user_message})
        logger.info(f'GPT запрос {user_message[:20]}')

        response = await cliet.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.8
        )

        answer = response.choices[0].message.content
        logger.info(f'GPT запрос {len(answer)}')
        return answer

    except Exception as e:
        logger.error(f'Ошибка GPT {e}')
        return f'Ошибка при обращении к GPT'


async def main():
    answer = await ask_gpt(user_message='Привет')
    print(answer)

asyncio.run(main())