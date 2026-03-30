from aiogram import Router
from handlers.commands_handlers import router as commands_router
from handlers.random_fact import router as random_fact_router
from handlers.gpt_chat import router as gpt_router

router = Router()

router.include_routers(commands_router, random_fact_router, gpt_router)