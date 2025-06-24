
from typing import List, Optional
import concurrent.futures
from config.settings import Settings
from core.entities.claim import Claim
from core.entities.knowledge_source import KnowledgeSource
from core.entities.news import News
from core.entities.retrieved_news import RetrievedNews
from core.entities.veredict import Veredict
from core.interfaces.i_model_service import IModelService
from core.interfaces.i_news_service import INewsService
from core.interfaces.respository import Repository
from typing import List, Tuple, Dict, Any, Callable

from infrastructure.services.model_service import ModelService
from infrastructure.services.news_service import NewsService
from infrastructure.utilities import AsyncThreadList




class NewsController:
    """Casos de uso - Lógica de aplicación"""

    _knowledge_source_international:list[KnowledgeSource]
    _knowledge_source_national:list[KnowledgeSource]
    _news_service: INewsService
    _model_service: IModelService
    model_async_list:AsyncThreadList
    
    def __init__(self,settings:Settings):
        self.settings = settings

    async def validate_news(self, text: str) -> News:

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers_principal) as executor:
            # Lanzar ambas tareas en paralelo
            future_comprobacion = executor.submit( self.semantic_comprobation, text)
            future_division = executor.submit( self.divide_in_claims, text)
            
            # Recoger resultados
            semantic_veredict, semantic_score = future_comprobacion.result()
            secciones, tiempo_division = future_division.result()
        
        await self._analizar_secciones_paralelo(secciones, self.news_content_comprobation)
        true_counter,false_counter = self.read_claims(secciones,self.min_claim_score)
        content_veredict,content_score = self.vote_claims(true_counter, false_counter,len(secciones))
        return_news = News(text,semantic_veredict, semantic_score,content_veredict,content_score)
        return_news.claims = secciones
        return_news.general_veredict = self.general_veredict(semantic_veredict, semantic_score,content_veredict,content_score)

        return return_news 
    
    def general_veredict(self,semantic_veredict:Veredict, semantic_score,content_veredict:Veredict,content_score)->Veredict:
        if semantic_veredict.is_true() and semantic_score > self.min_semantic_score and content_veredict.is_true():
            return Veredict(Veredict.TRUE_STATE)
        if semantic_veredict.is_true() and content_veredict.is_false():
            return Veredict(Veredict.FAKE_STATE)
        if semantic_veredict.is_false() and content_veredict.is_false():
            return Veredict(Veredict.FAKE_STATE)
        if semantic_veredict.is_false() and content_veredict.is_true():
            return Veredict(Veredict.TRUE_STATE)
        if semantic_veredict.is_not_verified() and content_veredict.is_true():
            return Veredict(Veredict.TRUE_STATE)
        if semantic_veredict.is_not_verified() and content_veredict.is_false():
            return Veredict(Veredict.FAKE_STATE)
        if semantic_veredict.is_false() and semantic_score > self.min_semantic_score and content_veredict.is_not_verified():
            return Veredict(Veredict.FAKE_STATE)
        if semantic_veredict.is_not_verified() and content_veredict.is_not_verified():
            return Veredict(Veredict.NO_VALIDATION_STATE)
        return Veredict(Veredict.NO_VALIDATION_STATE)
      

    
    def vote_claims(self,true_counter, false_counter,total_claims)->Tuple[Veredict,float]:
        true_prop = true_counter / total_claims
        false_prop = false_counter / total_claims
        if false_prop > self.min_news_false_score and false_counter > true_counter:
            veredict = Veredict(Veredict.FAKE_STATE)
        elif true_prop > self.min_news_true_score and true_counter > false_counter and true_counter > (total_claims-false_counter-true_counter):
            veredict = Veredict(Veredict.TRUE_STATE)
        else:
            veredict = Veredict(Veredict.NO_VALIDATION_STATE)
        return veredict,true_prop
        
        
        
    
    def read_claims(self,secciones:list[Claim])->Tuple[int,int]:
        true_counter = 0
        false_counter = 0
        for seccion in secciones:
            seccion:Claim
            if (seccion.veredict.is_true() and seccion.score > self.min_claim_score):
                true_counter += 1
            elif (seccion.veredict.is_false() and seccion.score > self.min_claim_score):
                false_counter += 1
        return true_counter,false_counter
    
    def claim_paralel_analysis(self, secciones: List[Claim], funcion_analisis: Callable) -> List[Any]:
        """Llamar a una búsqueda de contenido de cada claim en paralelo."""

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers_secciones) as executor:
            futures = [executor.submit(funcion_analisis, seccion) for seccion in secciones]
            resultados = [future.result() for future in futures]
        


    async def divide_in_claims(self, text:str) -> list[Claim]:
        return
    async def semantic_comprobation(self,text:str) -> Tuple[Veredict,float]:
        return
    def news_content_comprobation(self,claim: Claim):
        """Comprobar si cada claim es nacional o no y lanzar una lista de threads para cada medio"""
        if self.global_check(claim):
            news_source = self._knowledge_source_international
        else:
            news_source = self._knowledge_source_national
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.media_source_number) as executor:
            futures = [executor.submit(self.article_content_comprobation, claim, source) for source in news_source]
            resultados = [future.result() for future in futures]    
        claim.veredict,claim.score = self.voting_sistem(resultados)
       
    def article_content_comprobation(self,claim:Claim,source:KnowledgeSource) -> List[Veredict]:
        """Buscar noticias y lanzar un hilo para comprobar cada una de ellas"""
        news = self.search_news(self.number_news_per_source,claim,source)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.number_news_per_source) as executor:
            futures = [executor.submit(self.content_validation, claim, new, self.model_async_list) for new in news]
            resultados = [future.result() for future in futures]  
        return resultados
       

    def search_news(number_news:int,claim:Claim,source:KnowledgeSource) -> list[RetrievedNews]:
        #usar news service
        #si la knowledge source que se va a usar es international, traducir claim
        new_keywords = translator(keywords, max_length=len(keywords))[0]['translation_text']
        return
    def voting_sistem(self,validation_results:list[Veredict]) -> Tuple[Veredict,float]:

        true = sum(1 for result in validation_results if result.is_true)
        false = sum(1 for result in validation_results if result.is_false)
        no_val = len(validation_results) - true - false

        true_prop = true / (true+false+no_val)
        veredict= self.determine_veredict(true,false,no_val)

        return veredict,true_prop
    
    def determine_veredict(self,true:int,false:int,no_val:int) -> Veredict:
        true_prop = true / (true+false+no_val)
        false_prop = false / (true+false+no_val)
        if false_prop > self.min_false_prop and false > true:
            veredict = Veredict(Veredict.FAKE_STATE)
        elif true_prop > self.min_true_prop and true > false and true > no_val:
            veredict = Veredict(Veredict.TRUE_STATE)
        else:
            veredict = Veredict(Veredict.NO_VALIDATION_STATE)
        return veredict

    async def content_validation(input:str, news:RetrievedNews, list:AsyncThreadList) -> Veredict:
        """Contrastar una afirmación con un texto"""
        # usar check service
        # model_service (list)
        return
    
    async def global_check(claim) -> bool:
        #model_service
        # usar check service
        return 
    