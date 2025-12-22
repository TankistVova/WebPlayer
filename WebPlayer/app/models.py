from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TitleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    poster_url: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None


class Title(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    poster_url: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    created_at: datetime


class VideoQuality(BaseModel):
    quality: str  # "480p", "720p", "1080p", etc.
    url: str
    size_mb: Optional[int] = None


class EpisodeCreate(BaseModel):
    title_id: int
    season: int
    episode: int
    name: str
    qualities: List[VideoQuality]  # Список качеств
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None


class Episode(BaseModel):
    id: int
    title_id: int
    season: int
    episode: int
    name: str
    qualities: List[VideoQuality]
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    created_at: datetime
    
    @property
    def url(self) -> str:
        """Возвращает URL лучшего качества для совместимости"""
        if not self.qualities:
            return ""
        # Сортируем по качеству (1080p > 720p > 480p)
        sorted_qualities = sorted(self.qualities, key=lambda x: int(x.quality.replace('p', '')), reverse=True)
        return sorted_qualities[0].url


# Старые модели для совместимости
class VideoCreate(BaseModel):
    title: str
    url: str
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    qualities: Optional[List[VideoQuality]] = None


class Video(BaseModel):
    id: int
    title: str
    url: str
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    qualities: Optional[List[VideoQuality]] = None
    created_at: datetime