from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from core.entities.claim import Claim
from core.entities.knowledge_source import KnowledgeSource
from core.entities.retrieved_news import RetrievedNews
from core.entities.veredict import Veredict
from core.interfaces import i_LLM
from core.interfaces.i_embedding_service import IEmbeddingService
from core.interfaces.i_index_service import IIndexService
from infrastructure.database.index import Index
from infrastructure.database.vectorial_index import VectorialIndex

from infrastructure.utilities import AsyncThreadList


class IndexService(IIndexService):


    def index_search(self, query:str,vector_index:VectorialIndex,index:Index,embedding_service:IEmbeddingService,min_dist)-> str:


        query_embedding = embedding_service.get_embeddings(query)

        score,index_pos = vector_index.search_index(query_embedding)
        if score[0][0] > min_dist:
            return ''
        else:
            return index.search_index_position_url(index_pos[0][0])

