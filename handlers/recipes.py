import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import get_main_keyboard, get_back_keyboard
from states import UserStates
from services import RecipeService, translator
from utils import format_recipe

router = Router()
recipe_service = RecipeService()
logger = logging.getLogger(__name__)


@router.message(F.text == "🍳 Найти рецепт")
async def start_recipe_search(message: Message, state: FSMContext):
    """Начало поиска рецепта"""
    logger.info(f"🍳 Пользователь {message.from_user.id} начал поиск рецептов")
    
    await state.set_state(UserStates.waiting_for_recipe_query)
    logger.debug(f"  FSM состояние: waiting_for_recipe_query")
    
    await message.answer(
        "🔍 Отлично! Введите название блюда или ингредиенты.\n\n"
        "Примеры:\n"
        "• Паста карбонара\n"
        "• Блюда с курицей\n"
        "• Десерт с шоколадом\n"
        "• chicken pasta\n\n"
        "Напишите ваш запрос:",
        reply_markup=get_back_keyboard()
    )


@router.message(UserStates.waiting_for_recipe_query)
async def process_recipe_query(message: Message, state: FSMContext):
    """Обработка запроса рецепта"""
    
    # Проверка на кнопку "Назад"
    if message.text == "◀️ Назад":
        await state.set_state(UserStates.main_menu)
        await message.answer(
            "Главное меню 🏠",
            reply_markup=get_main_keyboard()
        )
        return
    
    query = message.text.strip()
    logger.info(f"🔍 Поиск рецептов по запросу: '{query}'")
    
    if not query:
        logger.warning(f"⚠️ Пустой запрос от пользователя {message.from_user.id}")
        await message.answer("Пожалуйста, введите запрос для поиска рецептов.")
        return
    
    # Показываем индикатор загрузки
    await message.answer("🔍 Ищу рецепты... Подождите немного.")
    
    # Переводим запрос на английский для API
    query_en = translator.translate_to_english(query)
    logger.info(f"🌐 Запрос переведен: '{query}' → '{query_en}'")
    
    # Получаем рецепты
    logger.debug(f"📡 Отправка запроса в RecipeService...")
    recipes = await recipe_service.search_recipes(query_en, max_results=5)
    logger.info(f"✅ Получено рецептов: {len(recipes)}")
    
    if not recipes:
        await message.answer(
            "😔 К сожалению, не удалось найти рецепты по вашему запросу.\n\n"
            "Попробуйте:\n"
            "• Использовать другие ключевые слова\n"
            "• Написать запрос на английском языке\n"
            "• Указать конкретное название блюда\n\n"
            "Введите новый запрос или нажмите '◀️ Назад':"
        )
        return
    
    # Отправляем найденные рецепты
    await message.answer(f"✅ Найдено рецептов: {len(recipes)}\n")
    
    for i, recipe in enumerate(recipes, 1):
        # Переводим рецепт на русский
        recipe_translated = {
            'title': translator.translate_to_russian(recipe.get('title', '')),
            'servings': recipe.get('servings', ''),
            'ingredients': translator.translate_to_russian(recipe.get('ingredients', '')),
            'instructions': translator.translate_to_russian(recipe.get('instructions', ''))
        }
        
        formatted_recipe = format_recipe(recipe_translated)
        
        try:
            await message.answer(
                f"<b>Рецепт {i}/{len(recipes)}</b>\n\n{formatted_recipe}",
                parse_mode="HTML"
            )
        except Exception as e:
            # Если возникла ошибка с форматированием, отправляем без HTML
            logger.error(f"Ошибка форматирования рецепта: {e}")
            await message.answer(
                f"Рецепт {i}: {recipe_translated.get('title', 'Без названия')}\n\n"
                f"{recipe_translated.get('instructions', 'Инструкции не найдены')}"
            )
    
    # Предлагаем продолжить или вернуться
    await message.answer(
        "Хотите найти ещё рецепты? Введите новый запрос или нажмите '◀️ Назад':",
        reply_markup=get_back_keyboard()
    )

