
import configparser

import pandas as pd
from config.settings import Settings
from core.controllers.news_controller import NewsController
from core.entities.knowledge_source import KnowledgeSource
from core.entities.news import News
from core.entities.veredict import Veredict
from infrastructure.factories.LLMFactory import LLMFactory
from infrastructure.services.embedding_service import EmbeddingService
from infrastructure.services.index_service import IndexService
from infrastructure.services.model_service import ModelService
from infrastructure.services.news_service import NewsService
from config.knowledge_source_list import knowledge_sources
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import Settings

import unittest
import time

from core.controllers.news_controller_linear import NewsControllerLinear

class test_NewsControllerLinear(unittest.TestCase):
    config = {
        "min_news_score": [0.1, 0.2, 0.3],
        "min_prop": [0.1, 0.2, 0.3],
        "min_claim_score": [0.1, 0.2, 0.3],
        "min_cos_dist": [ 10.0, 15.0, 20.0]
    }
    
    

    settings: Settings
    
    news_controller:NewsControllerLinear
    

    
    def setUp(self):
        self.settings = Settings()
        self.df = pd.read_csv('news.csv',sep=';')
        return super().setUp()
    
    def test_news_controller(self):
        inicio = time.time()
        controller = NewsControllerLinear(self.settings)
        self.dependency_injection(controller)
        news:News = controller.validate_news(self.query)
        tiempoTotal = time.time() -inicio

        print(f"Tiempo de ejecución {tiempoTotal}")
        print(f"Score de contenido {news.content_score}")
        self.assertTrue(news.general_veredict.state == Veredict.TRUE_STATE)
    
    def dependency_injection(self,controller:NewsControllerLinear):        
        controller._model_service = ModelService(LLMFactory.create_llm('local',self.settings),self.settings)
        controller._news_service = NewsService(self.settings)
        controller._embedding_service = EmbeddingService(self.settings)
        controller._knowledge_source_national, controller._knowledge_source_international = self.read_knowledge_list()
        controller._index_service = IndexService()
    
    def read_knowledge_list(self):
        sources = [KnowledgeSource(**data) for data in knowledge_sources]
        national = []
        for source in sources:
            if not source.international:
                national.append(source)
        return national,sources
    
    def test_short(self):
        
        controller = NewsControllerLinear(self.settings)
        self.dependency_injection(controller)
        text = self.df.iloc[6]['text']
        self.assertTrue(Veredict.TRUE_STATE == self.df.iloc[6]['label'])
        inicio = time.time()
        news:News = controller.validate_news(text)   
        tiempoTotal = time.time() -inicio
        print(f"Tiempo de ejecución {tiempoTotal}")
        print(f"Score de contenido {news.content_score}")
        self.assertTrue(Veredict.TRUE_STATE == news.general_veredict.state)     

    
    def test_long(self):
        
        controller = NewsControllerLinear(self.settings)
        self.dependency_injection(controller)
        
        log_pruebas = 'pruebas_parámetros.csv'
        with open(log_pruebas, 'w', encoding='utf-8') as f:
            f.write("time;min_news_score;min_prop;min_cos_dist;true_postive;false_positive;true_negative;false_negative;accuracy;not_verified\n")
        f.close()
        for min_news_score in self.config['min_news_score']:
            for min_prop in self.config['min_prop']:
                for min_cos_dist in self.config['min_cos_dist']:
                    controller.settings.min_news_score = min_news_score
                    controller.settings.min_prop = min_prop
                    controller.settings.min_cos_dist = min_cos_dist
                    true_positive = 0
                    false_positive = 0
                    true_negative = 0
                    false_negative = 0
                    inicio = time.time()
                    not_verified = 0
                    accuracy = 0
                    #bucle leyendo todas las noticias
                    for index, row in self.df.iterrows():
                        noticia = row['text']
                        news:News = controller.validate_news(noticia)
                        if news.general_veredict.is_true():
                            if news.general_veredict.state == row['label']:
                                true_positive += 1
                            else:
                                false_positive += 1
                        elif news.general_veredict.is_false():
                            if news.general_veredict.state == row['label']:
                                true_negative += 1
                            else:
                                false_negative += 1                     
                        else:
                            not_verified+=1
                    tiempoTotal = time.time() -inicio
                    if (true_positive+true_negative+false_positive+false_negative) > 0:
                        accuracy = (true_positive+true_negative)/(true_positive+true_negative+false_positive+false_negative)
                    with open(log_pruebas, 'a', encoding='utf-8') as f:
                        f.write(f"{tiempoTotal};{min_news_score};{min_prop};{min_cos_dist};{true_positive};{false_positive};{true_negative};{false_negative};{accuracy};{not_verified}\n")
    
    if __name__ == '__main__':
        unittest.main()