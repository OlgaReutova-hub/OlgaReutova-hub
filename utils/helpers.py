def format_recipe(recipe: dict) -> str:
    """Форматирует рецепт для отображения"""
    title = recipe.get('title', 'Без названия')
    ingredients = recipe.get('ingredients', '')
    servings = recipe.get('servings', 'Не указано')
    instructions = recipe.get('instructions', 'Инструкции не найдены')
    
    text = f"🍳 <b>{title}</b>\n\n"
    text += f"👥 <b>Порций:</b> {servings}\n\n"
    
    if ingredients:
        text += f"📝 <b>Ингредиенты:</b>\n{ingredients}\n\n"
    
    text += f"📖 <b>Приготовление:</b>\n{instructions}"
    
    return text


def format_nutrition_info(items: list) -> str:
    """Форматирует информацию о калориях"""
    if not items:
        return "❌ Не удалось найти информацию о калориях"
    
    text = "📊 <b>Пищевая ценность:</b>\n\n"
    
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    for item in items:
        name = item.get('name', 'Продукт')
        calories = item.get('calories', 0)
        protein = item.get('protein_g', 0)
        carbs = item.get('carbohydrates_total_g', 0)
        fat = item.get('fat_total_g', 0)
        serving = item.get('serving_size_g', 100)
        
        total_calories += calories
        total_protein += protein
        total_carbs += carbs
        total_fat += fat
        
        text += f"🔹 <b>{name.capitalize()}</b> ({serving}г)\n"
        text += f"   • Калории: {calories:.1f} ккал\n"
        text += f"   • Белки: {protein:.1f}г\n"
        text += f"   • Углеводы: {carbs:.1f}г\n"
        text += f"   • Жиры: {fat:.1f}г\n\n"
    
    if len(items) > 1:
        text += f"<b>📈 Итого:</b>\n"
        text += f"   • Калории: {total_calories:.1f} ккал\n"
        text += f"   • Белки: {total_protein:.1f}г\n"
        text += f"   • Углеводы: {total_carbs:.1f}г\n"
        text += f"   • Жиры: {total_fat:.1f}г\n"
    
    return text

