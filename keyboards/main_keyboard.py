from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard():
    """Главная клавиатура бота"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍳 Найти рецепт"), KeyboardButton(text="📊 Подсчитать калории")],
            [KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )


def get_calorie_input_keyboard():
    """Клавиатура для выбора способа ввода блюда"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✍️ Ввести текстом"), KeyboardButton(text="📸 Отправить фото")],
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )


def get_back_keyboard():
    """Клавиатура с кнопкой назад"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="◀️ Назад")]
        ],
        resize_keyboard=True
    )
