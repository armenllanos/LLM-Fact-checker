from typing import List, Optional
from core.entities.news import News
from core.interfaces.respository import Repository
from sqlalchemy.orm import Session
from sqlalchemy import select

from infrastructure.database.models import NewsModel, UserModel

class SQLNewsRepository(Repository):
    """Implementación concreta del repositorio con SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    async def create(self, news: News) -> News:
        db_news = NewsModel(
            id= news.id,
            content_veredict= news.content_veredict,
            content_score= news.content_score,
            semantic_veredict= news.semantic_veredict,
            semantic_score= news.semantic_score,
            general_veredict= news.general_veredict,
            created_at= news.created_at.isoformat()
        )
        self.db.add(db_news)
        self.db.commit()
        self.db.refresh(db_news)
        
        return News(
            id= db_news.id,
            content_veredict= db_news.content_veredict,
            content_score= db_news.content_score,
            semantic_veredict= db_news.semantic_veredict,
            semantic_score= db_news.semantic_score,
            general_veredict= db_news.general_veredict,
            created_at= db_news.created_at.isoformat()
        )
    
    async def get_by_id(self, user_id: int) -> Optional[News]:
        return

    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return
    
    async def update(self, user: User) -> User:
        return
    
    async def delete(self, user_id: int) -> bool:
        return