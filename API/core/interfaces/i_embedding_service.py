from abc import ABC, abstractmethod


class IEmbeddingService(ABC):
    
    embedding_model:str
    
    @abstractmethod
    def get_embeddings(self,text:str):
        pass