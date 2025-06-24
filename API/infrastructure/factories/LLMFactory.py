from config.settings import Settings
from core.entities.gemma import GemmaLLM
from core.entities.local_gemma import LocalGemmaLLM
from core.interfaces import i_LLM


class LLMFactory:
    @staticmethod
    def create_llm(tipo, settings:Settings)->i_LLM:
        if tipo=='mistral':
            return
        elif tipo=='gemma':
            return GemmaLLM(settings.gemma_api_key,settings.gemma_model_name)
        elif tipo=='local':
            return LocalGemmaLLM(settings.api_url,settings.api_model_name)

