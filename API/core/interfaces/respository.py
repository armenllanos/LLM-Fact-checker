
from abc import ABC, abstractmethod
from typing import List, Optional

from core.entities.news import News


class Repository(ABC):
    """Interface del repositorio - Define el contrato"""
    
    @abstractmethod
    async def create(self, news: News) -> News:
        pass
    
    @abstractmethod
    async def get_by_id(self, news_id: int) -> Optional[News]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[News]:
        pass
    
    @abstractmethod
    async def update(self, news: News) -> News:
        pass
    
    @abstractmethod
    async def delete(self, news_id: int) -> bool:
        pass