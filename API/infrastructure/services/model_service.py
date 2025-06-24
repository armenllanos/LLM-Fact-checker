import aiohttp
import asyncio
from typing import List, Dict, Any

from config.settings import Settings
from core.entities.claim import Claim
from core.entities.knowledge_source import KnowledgeSource
from core.entities.retrieved_news import RetrievedNews
from core.entities.veredict import Veredict

from core.interfaces.i_LLM import i_LLM
from core.interfaces.i_model_service import IModelService
from core.interfaces.i_news_service import INewsService
from infrastructure.factories import LLMFactory
from infrastructure.utilities import AsyncThreadList


class ModelService(IModelService):
    
    llm:i_LLM
    def __init__(self,llm:i_LLM,settings:Settings):
        self.llm = llm
        self.settings = settings
        
    def content_validation(self, query:str,content:str) -> Veredict:
        system_message = self.settings.content_validation_prompt
        full_input = "Afirmación:"+query+"Texto de referencia:"+content
        return Veredict(self.llm.ask_model(system_message,full_input))
       
        
    def is_global(self, query:str) -> bool:
        system_message = self.settings.is_global_prompt
        veredict = self.llm.ask_model(system_message,query)
        veredict = veredict.replace('\n', '')
        return veredict == self.settings.international_response

    def claim_extractor(self, query:str) -> list[Claim]:
        system_message = self.settings.claim_extractor_prompt
        claim_string = self.llm.ask_model(system_message,query)
        cliam_list = claim_string.split(';')
        result = []
        for claim_text in cliam_list:
            aux_claim = Claim(claim_text)
            result.append(aux_claim)
        return result