import logging
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)


class TranslatorService:
    """Сервис для перевода текста"""
    
    def __init__(self):
        logger.info("🌐 Инициализация сервиса перевода...")
        self.translator_to_en = GoogleTranslator(source='ru', target='en')
        self.translator_to_ru = GoogleTranslator(source='en', target='ru')
        logger.info("✅ Сервис перевода готов (GoogleTranslator)")
    
    def translate_to_english(self, text: str) -> str:
        """Переводит текст с русского на английский"""
        try:
            if not text or not text.strip():
                return text
            
            logger.debug(f"Перевод на английский: '{text}'")
            translated = self.translator_to_en.translate(text)
            logger.debug(f"Результат перевода: '{translated}'")
            return translated
        except Exception as e:
            logger.error(f"Ошибка перевода на английский: {e}")
            return text  # Возвращаем оригинал если не получилось
    
    def translate_to_russian(self, text: str) -> str:
        """Переводит текст с английского на русский"""
        try:
            if not text or not text.strip():
                return text
            
            logger.debug(f"Перевод на русский: '{text[:50]}...'")
            translated = self.translator_to_ru.translate(text)
            logger.debug(f"Результат перевода: '{translated[:50]}...'")
            return translated
        except Exception as e:
            logger.error(f"Ошибка перевода на русский: {e}")
            return text  # Возвращаем оригинал если не получилось


# Создаем единственный экземпляр
translator = TranslatorService()

