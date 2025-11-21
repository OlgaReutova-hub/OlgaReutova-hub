import logging
import aiohttp
from typing import List, Dict, Optional
from config import settings

logger = logging.getLogger(__name__)


class RecipeService:
    """Сервис для работы с API рецептов"""
    
    def __init__(self):
        self.api_url = settings.RECIPE_API_URL
        self.api_key = settings.CALORIE_NINJAS_API_KEY
        self.headers = {'X-Api-Key': self.api_key}
    
    async def search_recipes(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Поиск рецептов по запросу
        
        Args:
            query: Поисковый запрос
            max_results: Максимальное количество результатов
            
        Returns:
            Список рецептов
        """
        try:
            params = {'query': query}
            logger.info(f"🌐 Запрос к Recipe API: {self.api_url}")
            logger.debug(f"   Параметры: {params}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_url,
                    headers=self.headers,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    logger.info(f"📡 Ответ от API: статус {response.status}")
                    
                    if response.status == 200:
                        recipes = await response.json()
                        logger.info(f"✅ Получено рецептов: {len(recipes) if isinstance(recipes, list) else 0}")
                        return recipes[:max_results] if isinstance(recipes, list) else []
                    else:
                        response_text = await response.text()
                        logger.error(f"❌ Ошибка API: статус {response.status}")
                        logger.error(f"   Ответ: {response_text[:200]}")
                        return []
        except Exception as e:
            logger.error(f"❌ Ошибка при поиске рецептов: {e}", exc_info=True)
            return []
    
    async def get_recipe_by_ingredients(self, ingredients: List[str]) -> List[Dict]:
        """
        Поиск рецептов по ингредиентам
        
        Args:
            ingredients: Список ингредиентов
            
        Returns:
            Список рецептов
        """
        query = " ".join(ingredients)
        return await self.search_recipes(query)

