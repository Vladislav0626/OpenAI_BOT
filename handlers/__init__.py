from aiogram import Router
from handlers.commands_handlers import router as commands_router


router = Router()

router.include_routers(commands_router)