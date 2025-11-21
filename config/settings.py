import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Settings:
    """Настройки бота"""
    
    # Токен телеграм бота (из .env)
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # API ключ CalorieNinjas (из .env)
    CALORIE_NINJAS_API_KEY = os.getenv("CALORIE_NINJAS_API_KEY")
    
    # URL для API
    RECIPE_API_URL = "https://api.api-ninjas.com/v1/recipe"
    NUTRITION_API_URL = "https://api.api-ninjas.com/v1/nutrition"
    
    # Настройки
    MAX_RECIPES = 5
    CACHE_DIR = Path("cache")
    
    def __init__(self):
        # Создаем директорию для кэша
        self.CACHE_DIR.mkdir(exist_ok=True)
        
        # Проверяем наличие обязательных переменных окружения
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не найден в переменных окружения! Создайте файл .env")
        if not self.CALORIE_NINJAS_API_KEY:
            raise ValueError("CALORIE_NINJAS_API_KEY не найден в переменных окружения! Создайте файл .env")

