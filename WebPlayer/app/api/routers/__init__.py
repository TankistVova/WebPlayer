from fastapi import APIRouter

from .videos import router as videos_router
from .titles import router as titles_router
from .episodes import router as episodes_router


main_router = APIRouter()
main_router.include_router(videos_router)
main_router.include_router(titles_router)
main_router.include_router(episodes_router)
