import json
import faiss
import numpy as np


class VectorialIndex():
    index_path:str
    
    def __init__(self,index_path:str):
        self.index_path = index_path
        self._load_index()
        
    def _load_index(self):
        self.index = faiss.read_index(self.index_path)
            
    def update_index(self,new_vectors):
        self.index.add(np.array(new_vectors))
        faiss.write_index(self.index, self.index_path)
        
    def search_index(self,embedding,k=1):
        return self.index.search(np.array([embedding], dtype=np.float32), k)
    