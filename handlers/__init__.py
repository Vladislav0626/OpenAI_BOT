from handlers.commands_handlers import router as commands_router
from handlers.random_fact import router as random_fact_router
from handlers.gpt_chat import router as gpt_router
from handlers.talk import router as talk_router
from handlers.quiz import router as quiz_router
from handlers.economic_news import router as news_router

router = commands_router
router.include_router(random_fact_router)
router.include_router(gpt_router)
router.include_router(talk_router)
router.include_router(quiz_router)
router.include_routers(news_router)