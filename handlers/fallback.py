import logging
from aiogram import Router
from aiogram.types import Message

router = Router()
logger = logging.getLogger(__name__)


@router.message()
async def catch_all(message: Message):
    """Ловит все необработанные сообщения для отладки"""
    logger.warning(f"⚠️ Необработанное сообщение от {message.from_user.id}: '{message.text}'")
    await message.answer(
        f"Получено сообщение: {message.text}\n\n"
        "Используйте кнопки меню или /start для начала работы"
    )

