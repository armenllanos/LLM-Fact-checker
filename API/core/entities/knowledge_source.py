from infrastructure.database.index import Index
from infrastructure.database.vectorial_index import VectorialIndex


class KnowledgeSource:
    name:str
    international:bool
    url:str
    title_class:str
    resume_class:str
    body_class:str
    vector_index:VectorialIndex
    index:Index

    def __init__(self, name: str, international: bool, url: str,
        title_class: str, resume_class: str, body_class: str, index_path:str,vector_index_path:str):
        self.name = name
        self.international = international
        self.url = url
        self.title_class = title_class
        self.resume_class = resume_class
        self.body_class = body_class
        self.vector_index = VectorialIndex(vector_index_path)
        self.index = Index(index_path)