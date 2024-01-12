from fastapi import APIRouter, FastAPI

from src.app.comics.endpoints import router as comics_router
from src.app.images.endpoints import router as image_router
from src.app.translations.endpoints import router as translation_router


def register_routers(app: FastAPI):
    router = APIRouter(prefix="/api")

    router.include_router(comics_router)
    router.include_router(image_router)
    router.include_router(translation_router)

    app.include_router(router)
