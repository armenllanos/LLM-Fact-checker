from config.settings import Settings
from core.interfaces.i_embedding_service import IEmbeddingService
from sentence_transformers import SentenceTransformer

class EmbeddingService(IEmbeddingService):
    

    
    def __init__(self,settings:Settings):
        self.settings = settings
        self.modelo = SentenceTransformer(self.settings.embedding_model)
        
    def get_embeddings(self,text:str)->list[float]:
        
        return self.modelo.encode(text, convert_to_numpy=True)