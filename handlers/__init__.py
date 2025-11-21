from .start import router as start_router
from .recipes import router as recipes_router
from .calories import router as calories_router
from .fallback import router as fallback_router

__all__ = ['start_router', 'recipes_router', 'calories_router', 'fallback_router']

