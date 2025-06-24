
from typing import List, Optional
import concurrent.futures

from transformers import pipeline
from config.settings import Settings
from core.entities.claim import Claim
from core.entities.knowledge_source import KnowledgeSource
from core.entities.news import News
from core.entities.retrieved_news import RetrievedNews
from core.entities.veredict import Veredict
from core.interfaces.i_embedding_service import IEmbeddingService
from core.interfaces.i_index_service import IIndexService
from core.interfaces.i_model_service import IModelService
from core.interfaces.i_news_service import INewsService
from typing import List, Tuple, Dict, Any, Callable


class NewsControllerLinear:
    """Casos de uso - Lógica de aplicación"""

    _knowledge_source_international:list[KnowledgeSource]
    _knowledge_source_national:list[KnowledgeSource]
    _news_service: INewsService
    _model_service: IModelService
    _index_service: IIndexService
    _embedding_service: IEmbeddingService
    
    def __init__(self,settings:Settings):
        self.settings = settings
        self.translator = pipeline("translation", model=settings.translation_model_name,device='cpu')#"Helsinki-NLP/opus-mt-es-en"
        self.semantic_model = pipeline("text-classification", model=settings.semantic_model_name, tokenizer=settings.semantic_model_name)#"modelo_fake_news"
        

    def validate_news(self, text: str) -> News:

        secciones = self.divide_in_claims(text)
        semantic_veredict, semantic_score = self.semantic_comprobation(text)
        for seccion in secciones:
            self.news_content_comprobation_index(seccion)
        true_counter,false_counter = self.read_claims(secciones)
        content_veredict,content_score = self.vote_claims(true_counter, false_counter,len(secciones))
        return_news = News(text,semantic_veredict, semantic_score,content_veredict,content_score)
        return_news.claims = secciones
        return_news.content_score = content_score
        return_news.semantic_score = semantic_score
        return_news.general_veredict = self.general_veredict(semantic_veredict, semantic_score,content_veredict,content_score)

        return return_news 
    
    def general_veredict(self,semantic_veredict:Veredict, semantic_score,content_veredict:Veredict,content_score)->Veredict:
        if semantic_veredict.is_true() and semantic_score > self.settings.min_semantic_score and content_veredict.is_true():
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
        if semantic_veredict.is_false() and semantic_score > self.settings.min_semantic_score and content_veredict.is_not_verified():
            return Veredict(Veredict.FAKE_STATE)
        if semantic_veredict.is_not_verified() and content_veredict.is_not_verified():
            return Veredict(Veredict.NO_VALIDATION_STATE)
        if semantic_veredict.is_true() and content_veredict.is_not_verified():
            return Veredict(Veredict.TRUE_STATE)
        return Veredict(Veredict.NO_VALIDATION_STATE)
      

    
    def vote_claims(self,true_counter, false_counter,total_claims)->Tuple[Veredict,float]:
        true_prop = true_counter / total_claims
        false_prop = false_counter / total_claims
        if false_prop > self.settings.min_news_score and false_counter > true_counter:
            veredict = Veredict(Veredict.FAKE_STATE)
            return veredict,false_prop
        elif true_prop > self.settings.min_news_score and true_counter > false_counter:
            veredict = Veredict(Veredict.TRUE_STATE)
        else:
            veredict = Veredict(Veredict.NO_VALIDATION_STATE)
        return veredict,true_prop
        
        
        
    
    def read_claims(self,secciones:list[Claim])->Tuple[int,int]:
        true_counter = 0
        false_counter = 0
        for seccion in secciones:
            seccion:Claim
            if (seccion.veredict.is_true()):
                true_counter += 1
            elif (seccion.veredict.is_false()):
                false_counter += 1
        return true_counter,false_counter
    
    def claim_paralel_analysis(self, secciones: List[Claim], funcion_analisis: Callable) -> List[Any]:
        """Llamar a una búsqueda de contenido de cada claim en paralelo."""

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers_secciones) as executor:
            futures = [executor.submit(funcion_analisis, seccion) for seccion in secciones]
            resultados = [future.result() for future in futures]
        


    def divide_in_claims(self, text:str) -> list[Claim]:
        return self._model_service.claim_extractor(text)
       
    def semantic_comprobation(self,text:str) -> Tuple[Veredict,float]:
        max_len = 512
        evaluated_text = text[:max_len] if len(text) > max_len else text
        result = self.semantic_model(evaluated_text)
        if result[0]['label'] == 'True':
            return Veredict(Veredict.TRUE_STATE), float(result[0]['score'])
        else:
            return Veredict(Veredict.FAKE_STATE), float(result[0]['score'])
        
    def news_content_comprobation_scrapping(self,claim: Claim):
        """Comprobar si cada claim es nacional o no y lanzar una lista de threads para cada medio"""
        if self.global_check(claim):
            news_source = self._knowledge_source_international
        else:
            news_source = self._knowledge_source_national
        veredicts = []
        for source in news_source:
            veredicts.append(self.article_content_comprobation( claim, source))    
        claim.veredict,claim.score = self.voting_sistem(veredicts)
        
    def news_content_comprobation_index(self,claim: Claim):
        """Comprobar si cada claim es nacional o no y lanzar una lista de threads para cada medio"""
        if self.global_check(claim):
            news_source = self._knowledge_source_international
        else:
            news_source = self._knowledge_source_national
        veredicts = []
        for source in news_source:
            veredicts.append(self.indexed_content_comprobation( claim, source))    
        claim.veredict,claim.score = self.voting_sistem(veredicts)
       
    def article_content_comprobation(self,claim:Claim,source:KnowledgeSource) -> List[Veredict]:
        """Buscar noticias y lanzar un hilo para comprobar cada una de ellas"""
        news = self.search_news(self.settings.number_news_per_source,claim,source)
        content_veredicts = []
        for new in news:
            content_veredicts.append(self.content_validation(claim, new  )) 
        return content_veredicts

    def indexed_content_comprobation(self,claim:Claim,source:KnowledgeSource) -> Veredict:
        """Buscar noticias y lanzar un hilo para comprobar cada una de ellas"""
        news = self.search_index(self.settings.number_news_per_source,claim,source)
        if news and news.corpus:
            return self.content_validation(claim.text, news )
        else:
            return Veredict(Veredict.NO_VALIDATION_STATE)
    
    def search_index(self,number_news:int,claim:Claim,source:KnowledgeSource) -> RetrievedNews:

        claim_text = claim.text
        if source.international:
            claim_text = self.translator(claim.text, max_length=len(claim.text))[0]['translation_text']
        url = self._index_service.index_search(claim_text,source.vector_index,source.index,self._embedding_service,self.settings.min_cos_dist)
        if len(url) == 0:
            return
        return self._news_service.get_articles(url,source)

    def search_news(self,number_news:int,claim:Claim,source:KnowledgeSource) -> list[RetrievedNews]:

        claim_text = claim.text
        if source.international:
            claim_text = self.translator(claim.text, max_length=len(claim.text))[0]['translation_text']
        return self._news_service.get_news(source,claim_text,number_news,self.settings.min_cos_dist)


    def voting_sistem(self,validation_results:list[Veredict]) -> Tuple[Veredict,float]:

        true = sum(1 for result in validation_results if result.is_true())
        false = sum(1 for result in validation_results if result.is_false())
        no_val = len(validation_results) - true - false

        true_prop = true / (true+false+no_val)
        veredict= self.determine_veredict(true,false,no_val)

        return veredict,true_prop
    
    def determine_veredict(self,true:int,false:int,no_val:int) -> Veredict:
        true_prop = true / (true+false+no_val)
        false_prop = false / (true+false+no_val)
        if false_prop > self.settings.min_prop and false > true:
            veredict = Veredict(Veredict.FAKE_STATE)
        elif true_prop > self.settings.min_prop and true > false:
            veredict = Veredict(Veredict.TRUE_STATE)
        else:
            veredict = Veredict(Veredict.NO_VALIDATION_STATE)
        return veredict

    def content_validation(self, input:str, news:RetrievedNews) -> Veredict:
        """Contrastar una afirmación con un texto"""
        return self._model_service.content_validation(input,news.corpus)
    
    def global_check(self,claim:Claim) -> bool:
        return self._model_service.is_global(claim.text)
    