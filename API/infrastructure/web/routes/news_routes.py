from core.controllers.news_controller import  NewsController
from core.controllers.news_controller_linear import NewsControllerLinear
from core.entities.news import News
from core.entities.veredict import Veredict
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional


router = APIRouter(prefix="/news", tags=["news"])

# DTOs (Data Transfer Objects)
class UserCreate():
    name: str
    email: str

class NewsCreate():
    text: str


class UserUpdate():
    name: Optional[str] = None
    email: Optional[str] = None

class NewsResponse():
    id: int
    content_veredict: Veredict
    content_score: float
    semantic_veredict: Veredict
    semantic_score: float
    general_veredict: Veredict
    created_at: str
    

@router.post("/", response_model=NewsResponse, status_code=status.HTTP_201_CREATED)
async def validate_news(
    news_data: NewsCreate,
):
    """Validar una noticia"""
    try:
        news:News =  await controller.validate_news(news_data.text)
        return NewsResponse(
            id= news.id,
            content_veredict= news.content_veredict,
            content_score= news.content_score,
            semantic_veredict= news.semantic_veredict,
            semantic_score= news.semantic_score,
            general_veredict= news.general_veredict,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
