from typing import List

from fastapi import Depends, APIRouter, HTTPException

from ... import storage
from ..deps.auth import verify_token
from ...models import Episode, EpisodeCreate


router = APIRouter(prefix="/episodes", tags=["episodes"])


@router.get("/title/{title_id}", response_model=List[Episode])
def get_episodes_by_title(title_id: int):
    """Получить все эпизоды тайтла"""
    return storage.get_episodes_by_title(title_id)


@router.get("/{episode_id}", response_model=Episode)
def get_episode(episode_id: int):
    """Получить эпизод по ID"""
    episode = storage.get_episode_by_id(episode_id)
    if not episode:
        raise HTTPException(404, "Эпизод не найден")
    return episode


@router.post("", response_model=Episode)
def create_episode(episode: EpisodeCreate, token: str = Depends(verify_token)):
    """Добавить новый эпизод (требует авторизацию)"""
    # Проверяем существование тайтла
    if not storage.get_title_by_id(episode.title_id):
        raise HTTPException(404, "Тайтл не найден")
    return storage.create_episode(episode)


@router.delete("/{episode_id}")
def delete_episode(episode_id: int, token: str = Depends(verify_token)):
    """Удалить эпизод (требует авторизацию)"""
    if not storage.delete_episode(episode_id):
        raise HTTPException(404, "Эпизод не найден")
    return {"message": "Эпизод удален"}