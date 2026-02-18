from aiogram import Router
from .user import router as user_router

main_router = Router()
main_router.include_routers(user_router)
