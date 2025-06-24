from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from core.entities.claim import Claim
from core.entities.knowledge_source import KnowledgeSource
from core.entities.retrieved_news import RetrievedNews
from core.entities.veredict import Veredict
from core.interfaces import i_LLM
from infrastructure.utilities import AsyncThreadList


class IModelService(ABC):
    """Interface para llamada de modelos con distintos propósitos"""
    
    llm:i_LLM

    @abstractmethod
    def content_validation(self, query:str,content:str)-> Veredict:
        """Leer N noticias de un medio de comunicación"""
        pass
    @abstractmethod
    def is_global(self, query:str) -> bool:
        """Leer N noticias de un medio de comunicación"""
        pass
    @abstractmethod
    def claim_extractor(self, query:str) -> list[Claim]:
        """Leer N noticias de un medio de comunicación"""
        pass
    
