from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .routers import main_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Video Player API",
        description="Минималистичный API для веб-плеера видео",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Подключаем роутеры
    app.include_router(main_router)

    @app.get("/")
    def root():
        """Главная страница с веб-плеером"""
        return FileResponse("static/index.html")

    @app.get("/health")
    def health():
        """Проверка работоспособности API"""
        return {"status": "ok", "message": "Video Player API работает"}

    return app
