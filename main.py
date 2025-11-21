import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from handlers import start_router, recipes_router, calories_router, fallback_router


# Создаем папку для логов
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Имя файла лога с датой и временем
log_filename = logs_dir / f"bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Создаем форматтеры
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('[%(levelname)s] %(message)s')  # Упрощенный формат для консоли

# Обработчик для файла (с UTF-8 и эмодзи)
file_handler = logging.FileHandler(log_filename, encoding='utf-8')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.DEBUG)

# Обработчик для консоли (без эмодзи, с cp1251)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(console_formatter)
console_handler.setLevel(logging.INFO)

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler, console_handler]
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    
    logger.info("=" * 60)
    logger.info("🤖 ЗАПУСК ТЕЛЕГРАМ БОТА")
    logger.info("=" * 60)
    logger.info(f"📁 Лог файл: {log_filename}")
    logger.info(f"🔑 Токен бота: {settings.BOT_TOKEN[:10]}...{settings.BOT_TOKEN[-10:]}")
    logger.info(f"🔑 API ключ: {settings.CALORIE_NINJAS_API_KEY[:10]}...")
    
    try:
        # Инициализация бота и диспетчера
        logger.info("⚙️ Инициализация бота...")
        bot = Bot(token=settings.BOT_TOKEN)
        logger.info("✅ Бот инициализирован")
        
        logger.info("⚙️ Создание хранилища FSM...")
        storage = MemoryStorage()
        logger.info("✅ Хранилище создано")
        
        logger.info("⚙️ Создание диспетчера...")
        dp = Dispatcher(storage=storage)
        logger.info("✅ Диспетчер создан")
        
        # Подключение роутеров (ПОРЯДОК ВАЖЕН!)
        logger.info("📡 Подключение роутеров...")
        dp.include_router(start_router)
        logger.info("  ✓ start_router подключен")
        dp.include_router(recipes_router)
        logger.info("  ✓ recipes_router подключен")
        dp.include_router(calories_router)
        logger.info("  ✓ calories_router подключен")
        dp.include_router(fallback_router)  # ПОСЛЕДНИМ! Ловит необработанные
        logger.info("  ✓ fallback_router подключен (catch-all)")
        
        # Информация о запуске
        logger.info("=" * 60)
        logger.info("🚀 БОТ ЗАПУЩЕН И ГОТОВ К РАБОТЕ!")
        logger.info("=" * 60)
        logger.info("📱 Telegram: @AI_buter_bot")
        logger.info("🛑 Для остановки нажмите Ctrl+C")
        logger.info("=" * 60)
        
        # Удаление вебхуков (на случай если были)
        logger.info("🧹 Удаление старых вебхуков...")
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Вебхуки удалены")
        
        # Получение информации о боте
        logger.info("📊 Получение информации о боте...")
        me = await bot.get_me()
        logger.info(f"✅ Бот: @{me.username} (ID: {me.id})")
        logger.info(f"   Имя: {me.first_name}")
        
        # Запуск поллинга
        logger.info("🔄 Запуск polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ КРИТИЧЕСКАЯ ОШИБКА ПРИ ЗАПУСКЕ БОТА")
        logger.error("=" * 60)
        logger.exception(f"Ошибка: {e}")
        logger.error("=" * 60)
        raise
    finally:
        logger.info("🛑 Закрытие сессии бота...")
        try:
            await bot.session.close()
            logger.info("✅ Сессия закрыта")
        except Exception as e:
            logger.error(f"❌ Ошибка при закрытии сессии: {e}")


if __name__ == "__main__":
    try:
        logger.info("🎬 Запуск основной функции...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("=" * 60)
        logger.info("⚠️ ПОЛУЧЕН СИГНАЛ ОСТАНОВКИ (Ctrl+C)")
        logger.info("👋 Бот корректно остановлен")
        logger.info("=" * 60)
    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ НЕОЖИДАННАЯ ОШИБКА")
        logger.error("=" * 60)
        logger.exception(f"Ошибка: {e}")
        logger.error("=" * 60)

