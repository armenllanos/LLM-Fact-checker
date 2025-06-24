from config.settings import Settings
from core.controllers.news_controller import NewsController
from core.entities.knowledge_source import KnowledgeSource
from infrastructure.factories import LLMFactory
from infrastructure.services.model_service import ModelService
from infrastructure.services.news_service import NewsService
from config.knowledge_source_list import knowledge_sources
import pytest
import time

class TestNewsController:
    
    settings = Settings('appsettings.ini')
    
    text = """La caída de WhatsApp fue profetizada en la Biblia
        La tarde de este miércoles, el mundo se conmocionó ante la imposibilidad de usar la aplicación conocida como Whatsapp, el popular sistema de mensajería que se utiliza para estar comunicados en tiempo real con las personas queridas sin la molestia de tener que hablar con ellas.
        Muchos están desesperados porque no pueden comunicarse con sus contactos, ya no saben qué están haciendo, si ya comieron, si siguen en el trabajo, si van en el micro escuchando el Pasito perrón o si van en el taxi escuchando el Pasito a pasito, suave suavecito.
        Pero no es una simple falla esto que está ocurriendo: ya se hablaba en la Biblia de ello, en el libro de Proverbios, capítulo *NUMBER*, versículo *NUMBER*.
        "La vida y la muerte dependen de la lengua; los que hablan mucho sufrirán las consecuencias".
        Aquí, claramente habla de cómo los que usan más el Whatsapp están pasando por un duro momento, como si sus conversaciones fueran de vida o muerte. Pero, insistimos, esto es serio, y la Biblia lo sabe.
        Porque WhatsApp es tan importante ya, que hasta en el Apocalipsis, o Libro de las Revelaciones, es nombrado, en *NUMBER*:*NUMBER*
        "Después de estas cosas miré, y he aquí una gran multitud, la cual ninguno podía contar, de todas las naciones y tribus y pueblos y lenguas, que estaban delante del trono y en la presencia del Cordero, vestidos de ropas blancas y con palmas en sus manos".
        Es claro que están rogando que ya no se caiga WhatsApp.
        Mientras el sistema de dicha plataforma se corrige, muchos rezan porque esto sea sólo temporal y muy pronto todo vuelva a la normalidad."""
    
    def test_news_controller(self):
        inicio = time.time()
        controller = NewsController(self.settings)
        self.dependency_injection(controller)
        news = controller.validate_news("")
        tiempoTotal = time.time() -inicio

        print(f"Tiempo de ejecución {tiempoTotal}")
    
    def dependency_injection(self,controller:NewsController):        
        controller._model_service = ModelService(LLMFactory().create_llm('local',self.settings))
        controller._news_service = NewsService(self.settings)
        controller._knowledge_source_national, controller._knowledge_source_international = self.read_knowledge_list()
    
    def read_knowledge_list(self):
        sources = [KnowledgeSource(**data) for data in knowledge_sources]
        national = []
        for source in sources:
            if not source.international:
                national.append(source)
        return national,sources
    
    def long_test(self):
        return