from typing import List

from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException

from ... import storage
from ..deps.auth import verify_token
from ...models import Video
from ...models import VideoCreate


router = APIRouter(prefix="/videos", tags=["videos"])


@router.get("", response_model=List[Video])
def get_videos():
    """Получить список всех видео"""
    return storage.get_all()


@router.get("/{video_id}", response_model=Video)
def get_video(video_id: int):
    """Получить видео по ID"""
    video = storage.get_by_id(video_id)
    if not video:
        raise HTTPException(404, "Видео не найдено")
    return video


@router.post("", response_model=Video)
def create_video(video: VideoCreate, token: str = Depends(verify_token)):
    """Добавить новое видео (требует авторизацию)"""
    return storage.create(video)


@router.delete("/{video_id}")
def delete_video(video_id: int, token: str = Depends(verify_token)):
    """Удалить видео (требует авторизацию)"""
    if not storage.delete(video_id):
        raise HTTPException(404, "Видео не найдено")
    return {"message": "Видео удалено"}
