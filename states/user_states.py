from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    """Состояния пользователя в FSM"""
    
    # Главное меню
    main_menu = State()
    
    # Поиск рецептов
    waiting_for_recipe_query = State()
    
    # Подсчет калорий
    waiting_for_food_text = State()
    waiting_for_food_photo = State()

