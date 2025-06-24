from config.settings import Settings
from core.controllers.news_controller import NewsController
from core.controllers.news_controller_linear import NewsControllerLinear
from core.entities.knowledge_source import KnowledgeSource
from infrastructure.factories.LLMFactory import LLMFactory
from infrastructure.services.embedding_service import EmbeddingService
from infrastructure.services.index_service import IndexService
from infrastructure.services.model_service import ModelService
from infrastructure.services.news_service import NewsService
from config.knowledge_source_list import knowledge_sources

class Dependencies():
    @staticmethod
    def _dependency_injection(controller:NewsControllerLinear):
        controller._model_service = ModelService(LLMFactory.create_llm('local',controller.settings),controller.settings)
        controller._news_service = NewsService(controller.settings)
        controller._embedding_service = EmbeddingService(controller.settings)
        controller._knowledge_source_national, controller._knowledge_source_international = read_knowledge_list()
        controller._index_service = IndexService()
        
        
def read_knowledge_list():
    sources = [KnowledgeSource(**data) for data in knowledge_sources]
    national = []
    for source in sources:
        if not source.international:
            national.append(source)
    return national,sources
        