import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .models import Video, VideoCreate, Title, TitleCreate, Episode, EpisodeCreate

VIDEOS_FILE = Path("videos.json")
TITLES_FILE = Path("titles.json")
EPISODES_FILE = Path("episodes.json")


def load_data(file_path: Path) -> List[dict]:
    return json.load(open(file_path, encoding='utf-8')) if file_path.exists() else []


def save_data(data: List[dict], file_path: Path) -> None:
    json.dump(data, open(file_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2, default=str)


# Функции для тайтлов
def get_all_titles() -> List[Title]:
    return [Title(**item) for item in load_data(TITLES_FILE)]


def get_title_by_id(title_id: int) -> Optional[Title]:
    for item in load_data(TITLES_FILE):
        if item['id'] == title_id:
            return Title(**item)
    return None


def create_title(title_data: TitleCreate) -> Title:
    data = load_data(TITLES_FILE)
    new_id = max([item['id'] for item in data], default=0) + 1
    
    title = Title(
        id=new_id,
        created_at=datetime.now(),
        **title_data.model_dump()
    )
    
    data.append(title.model_dump())
    save_data(data, TITLES_FILE)
    return title


def delete_title(title_id: int) -> bool:
    data = load_data(TITLES_FILE)
    original_len = len(data)
    data = [item for item in data if item['id'] != title_id]
    
    if len(data) < original_len:
        save_data(data, TITLES_FILE)
        # Удаляем все эпизоды этого тайтла
        episodes_data = load_data(EPISODES_FILE)
        episodes_data = [item for item in episodes_data if item['title_id'] != title_id]
        save_data(episodes_data, EPISODES_FILE)
        return True
    return False


# Функции для эпизодов
def get_episodes_by_title(title_id: int) -> List[Episode]:
    episodes = [Episode(**item) for item in load_data(EPISODES_FILE) if item['title_id'] == title_id]
    return sorted(episodes, key=lambda x: (x.season, x.episode))


def get_episode_by_id(episode_id: int) -> Optional[Episode]:
    for item in load_data(EPISODES_FILE):
        if item['id'] == episode_id:
            return Episode(**item)
    return None


def create_episode(episode_data: EpisodeCreate) -> Episode:
    data = load_data(EPISODES_FILE)
    new_id = max([item['id'] for item in data], default=0) + 1
    
    episode = Episode(
        id=new_id,
        created_at=datetime.now(),
        **episode_data.model_dump()
    )
    
    data.append(episode.model_dump())
    save_data(data, EPISODES_FILE)
    return episode


def delete_episode(episode_id: int) -> bool:
    data = load_data(EPISODES_FILE)
    original_len = len(data)
    data = [item for item in data if item['id'] != episode_id]
    
    if len(data) < original_len:
        save_data(data, EPISODES_FILE)
        return True
    return False


# Старые функции для совместимости
def get_all() -> List[Video]:
    return [Video(**item) for item in load_data(VIDEOS_FILE)]


def get_by_id(video_id: int) -> Optional[Video]:
    for item in load_data(VIDEOS_FILE):
        if item['id'] == video_id:
            return Video(**item)
    return None


def create(video_data: VideoCreate) -> Video:
    data = load_data(VIDEOS_FILE)
    new_id = max([item['id'] for item in data], default=0) + 1
    
    video = Video(
        id=new_id,
        created_at=datetime.now(),
        **video_data.model_dump()
    )
    
    data.append(video.model_dump())
    save_data(data, VIDEOS_FILE)
    return video


def delete(video_id: int) -> bool:
    data = load_data(VIDEOS_FILE)
    original_len = len(data)
    data = [item for item in data if item['id'] != video_id]
    
    if len(data) < original_len:
        save_data(data, VIDEOS_FILE)
        return True
    return False