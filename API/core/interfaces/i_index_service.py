from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from core.entities.claim import Claim
from core.entities.knowledge_source import KnowledgeSource
from core.entities.retrieved_news import RetrievedNews
from core.entities.veredict import Veredict
from core.interfaces import i_LLM
from core.interfaces.i_embedding_service import IEmbeddingService
from infrastructure.database.index import Index
from infrastructure.database.vectorial_index import VectorialIndex
from infrastructure.utilities import AsyncThreadList


class IIndexService(ABC):

    @abstractmethod
    def index_search(self, query:str,vector_index:VectorialIndex,index:Index,embedding_service:IEmbeddingService,min_dist)-> str:
        """Buscar el titular más relacionado con una query"""
        pass

    
