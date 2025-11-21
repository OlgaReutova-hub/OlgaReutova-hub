import logging
import aiohttp
from typing import List, Dict, Optional
from config import settings

logger = logging.getLogger(__name__)


class CalorieService:
    """Сервис для подсчета калорий"""
    
    def __init__(self):
        self.api_url = settings.NUTRITION_API_URL
        self.api_key = settings.CALORIE_NINJAS_API_KEY
        self.headers = {'X-Api-Key': self.api_key}
    
    async def get_nutrition_info(self, food_query: str) -> List[Dict]:
        """
        Получает информацию о питательной ценности продуктов
        
        Args:
            food_query: Описание продуктов (например: "200g chicken breast and 1 apple")
            
        Returns:
            Список с информацией о калориях и БЖУ
        """
        try:
            params = {'query': food_query}
            logger.info(f"🌐 Запрос к Nutrition API: {self.api_url}")
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
                        data = await response.json()
                        logger.info(f"✅ Получено продуктов: {len(data) if isinstance(data, list) else 0}")
                        return data if isinstance(data, list) else []
                    else:
                        response_text = await response.text()
                        logger.error(f"❌ Ошибка API: статус {response.status}")
                        logger.error(f"   Ответ: {response_text[:200]}")
                        return []
        except Exception as e:
            logger.error(f"❌ Ошибка при получении информации о калориях: {e}", exc_info=True)
            return []
    
    async def analyze_meal(self, meal_description: str) -> Dict:
        """
        Анализирует блюдо и возвращает полную информацию
        
        Args:
            meal_description: Описание блюда
            
        Returns:
            Словарь с информацией о калориях
        """
        nutrition_data = await self.get_nutrition_info(meal_description)
        
        if not nutrition_data:
            return {
                'success': False,
                'message': 'Не удалось найти информацию о продуктах'
            }
        
        total_calories = sum(item.get('calories', 0) for item in nutrition_data)
        total_protein = sum(item.get('protein_g', 0) for item in nutrition_data)
        total_carbs = sum(item.get('carbohydrates_total_g', 0) for item in nutrition_data)
        total_fat = sum(item.get('fat_total_g', 0) for item in nutrition_data)
        
        return {
            'success': True,
            'items': nutrition_data,
            'totals': {
                'calories': total_calories,
                'protein': total_protein,
                'carbs': total_carbs,
                'fat': total_fat
            }
        }

