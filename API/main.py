
from fastapi import FastAPI, APIRouter, Depends, Form, HTTPException, status
from pydantic import BaseModel
import uvicorn
from config.settings import Settings
from core.controllers.news_controller_linear import NewsControllerLinear
from core.entities.news import News
from core.entities.veredict import Veredict
from infrastructure.web.dependencies import Dependencies

class NewsCreate(BaseModel):
    text: str

class NewsResponse(BaseModel):
    content_veredict: str
    content_score: float
    semantic_veredict: str
    semantic_score: float
    general_veredict: str




settings = Settings()
controller = NewsControllerLinear(settings)
Dependencies._dependency_injection(controller=controller)

# Crear aplicación FastAPI
app = FastAPI(
    title="Fack checking con LLM por medios de comunicación API",
    description="Fack checking con LLM por medios de comunicación",
    version="0.1.0"
)


@app.get("/")
async def root():
    return {"message": "Clean Architecture API funcionando"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/news", response_model=NewsResponse, status_code=status.HTTP_201_CREATED)
async def validate_news(
    news_data: NewsCreate = Form(),
):
    """Validar una noticia"""
    try:
        news:News = controller.validate_news(news_data.text)
        return NewsResponse(
            content_veredict= news.content_veredict.state,
            content_score= news.content_score,
            semantic_veredict= news.semantic_veredict.state,
            semantic_score= news.semantic_score,
            general_veredict= news.general_veredict.state,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)