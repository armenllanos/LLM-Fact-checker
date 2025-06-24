from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from core.entities.knowledge_source import KnowledgeSource
from core.entities.retrieved_news import RetrievedNews


class i_LLM(ABC):

    type:str
    
    @abstractmethod
    def ask_model(self,sytem_message,user_message) -> str:
        """LLamar a un modelo,  y que responde"""
        pass