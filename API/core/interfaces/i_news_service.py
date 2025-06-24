from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from core.entities.knowledge_source import KnowledgeSource
from core.entities.retrieved_news import RetrievedNews


class INewsService(ABC):
    """Interface para la lectura de noticias"""
    
    @abstractmethod
    def get_news(self, source: KnowledgeSource,query:str,number_of_news:int,min_cos_dist:float = 0) -> list[RetrievedNews]:
        """Leer N noticias de un medio de comunicación"""
        pass
    @abstractmethod
    def get_articles(self,url:str,source:KnowledgeSource)->RetrievedNews:
        """Leer una noticia de un medio de comunicación"""
        pass
