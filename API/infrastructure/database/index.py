import json


class Index():
    index_path:str
    
    def __init__(self,index_path:str):
        self.index_path = index_path
        self._load_index()
        
    def _load_index(self):
        with open(self.index_path, "r") as f:
            self.index = json.load(f)
            
    def update_index(self,new_index_intries):
        with open(self.index_path, "a") as f:
            json.dump(new_index_intries, f)
    
    def search_index_position_url(self,position,k=1):
        return self.index[position]['url']