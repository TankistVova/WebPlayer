from typing import List

from fastapi import Depends, APIRouter, HTTPException

from ... import storage
from ..deps.auth import verify_token
from ...models import Title, TitleCreate


router = APIRouter(prefix="/titles", tags=["titles"])


@router.get("", response_model=List[Title])
def get_titles():
    """Получить список всех тайтлов"""
    return storage.get_all_titles()


@router.get("/{title_id}", response_model=Title)
def get_title(title_id: int):
    """Получить тайтл по ID"""
    title = storage.get_title_by_id(title_id)
    if not title:
        raise HTTPException(404, "Тайтл не найден")
    return title


@router.post("", response_model=Title)
def create_title(title: TitleCreate, token: str = Depends(verify_token)):
    """Добавить новый тайтл (требует авторизацию)"""
    return storage.create_title(title)


@router.delete("/{title_id}")
def delete_title(title_id: int, token: str = Depends(verify_token)):
    """Удалить тайтл (требует авторизацию)"""
    if not storage.delete_title(title_id):
        raise HTTPException(404, "Тайтл не найден")
    return {"message": "Тайтл удален"}