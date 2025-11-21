import logging
from aiogram import Router, F
from aiogram.types import Message, PhotoSize
from aiogram.fsm.context import FSMContext
from pathlib import Path

from keyboards import (
    get_main_keyboard,
    get_calorie_input_keyboard,
    get_back_keyboard
)
from states import UserStates
from services import CalorieService, ImageAnalyzer
from utils import format_nutrition_info

router = Router()
calorie_service = CalorieService()
image_analyzer = ImageAnalyzer()
logger = logging.getLogger(__name__)


@router.message(F.text == "📊 Подсчитать калории")
async def start_calorie_count(message: Message, state: FSMContext):
    """Начало подсчета калорий"""
    logger.info(f"📊 Пользователь {message.from_user.id} начал подсчет калорий")
    
    await state.set_state(UserStates.main_menu)
    
    await message.answer(
        "📊 Выберите способ ввода информации о блюде:",
        reply_markup=get_calorie_input_keyboard()
    )


@router.message(F.text == "✍️ Ввести текстом")
async def request_food_text(message: Message, state: FSMContext):
    """Запрос текстового описания блюда"""
    await state.set_state(UserStates.waiting_for_food_text)
    
    await message.answer(
        "✍️ Опишите ваше блюдо.\n\n"
        "Для точного подсчета указывайте вес продуктов.\n\n"
        "Примеры:\n"
        "• 200g куриная грудка, 100g рис, салат\n"
        "• Яблоко 150г, банан\n"
        "• 300g pasta, 100g cheese\n"
        "• Борщ 400мл, хлеб 50г\n\n"
        "Напишите описание:",
        reply_markup=get_back_keyboard()
    )


@router.message(F.text == "📸 Отправить фото")
async def request_food_photo(message: Message, state: FSMContext):
    """Запрос фото блюда"""
    await state.set_state(UserStates.waiting_for_food_photo)
    
    await message.answer(
        "📸 Отправьте фотографию вашего блюда.\n\n"
        "⚠️ Обратите внимание:\n"
        "Для распознавания еды по фото требуется интеграция с AI моделью "
        "(OpenAI Vision, Google Cloud Vision и т.д.).\n\n"
        "После отправки фото вас попросят описать блюдо текстом "
        "для точного подсчета калорий.\n\n"
        "Отправьте фото или нажмите '◀️ Назад':",
        reply_markup=get_back_keyboard()
    )


@router.message(UserStates.waiting_for_food_text, F.text)
async def process_food_text(message: Message, state: FSMContext):
    """Обработка текстового описания блюда"""
    
    # Проверка на кнопку "Назад"
    if message.text == "◀️ Назад":
        await state.set_state(UserStates.main_menu)
        await message.answer(
            "📊 Выберите способ ввода информации о блюде:",
            reply_markup=get_calorie_input_keyboard()
        )
        return
    
    food_description = message.text.strip()
    
    if not food_description:
        await message.answer("Пожалуйста, опишите ваше блюдо.")
        return
    
    # Показываем индикатор загрузки
    await message.answer("⏳ Анализирую продукты и считаю калории...")
    
    # Получаем информацию о калориях
    nutrition_data = await calorie_service.get_nutrition_info(food_description)
    
    if not nutrition_data:
        await message.answer(
            "😔 Не удалось определить калории для указанных продуктов.\n\n"
            "Попробуйте:\n"
            "• Указать продукты более конкретно\n"
            "• Использовать английские названия\n"
            "• Разбить сложные блюда на отдельные ингредиенты\n\n"
            "Введите новое описание или нажмите '◀️ Назад':"
        )
        return
    
    # Форматируем и отправляем результат
    result_text = format_nutrition_info(nutrition_data)
    
    await message.answer(result_text, parse_mode="HTML")
    
    # Предлагаем продолжить
    await message.answer(
        "Хотите посчитать калории для другого блюда?\n"
        "Введите новое описание или нажмите '◀️ Назад':",
        reply_markup=get_back_keyboard()
    )


@router.message(UserStates.waiting_for_food_photo, F.photo)
async def process_food_photo(message: Message, state: FSMContext):
    """Обработка фото блюда"""
    
    # Получаем фото лучшего качества
    photo: PhotoSize = message.photo[-1]
    
    await message.answer("📸 Фото получено! Анализирую...")
    
    try:
        # Скачиваем файл
        file = await message.bot.get_file(photo.file_id)
        file_path = file.file_path
        
        # Сохраняем локально
        cache_dir = Path("cache")
        cache_dir.mkdir(exist_ok=True)
        local_path = cache_dir / f"{photo.file_id}.jpg"
        
        await message.bot.download_file(file_path, local_path)
        
        # Анализируем изображение
        analysis_result = await image_analyzer.analyze_food_image(str(local_path))
        
        # Удаляем временный файл
        if local_path.exists():
            local_path.unlink()
        
        if analysis_result:
            await message.answer(
                f"🤖 {analysis_result}\n\n"
                "Пожалуйста, опишите ваше блюдо текстом для точного подсчета калорий:",
                reply_markup=get_back_keyboard()
            )
            # Переводим в режим ожидания текста
            await state.set_state(UserStates.waiting_for_food_text)
        else:
            await message.answer(
                "❌ Ошибка при анализе изображения.\n"
                "Пожалуйста, опишите ваше блюдо текстом:",
                reply_markup=get_back_keyboard()
            )
            await state.set_state(UserStates.waiting_for_food_text)
            
    except Exception as e:
        print(f"Ошибка обработки фото: {e}")
        await message.answer(
            "❌ Произошла ошибка при обработке фото.\n"
            "Пожалуйста, опишите ваше блюдо текстом:",
            reply_markup=get_back_keyboard()
        )
        await state.set_state(UserStates.waiting_for_food_text)

