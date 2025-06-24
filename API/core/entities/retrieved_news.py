from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from core.entities.claim import Claim
from core.entities.knowledge_source import KnowledgeSource
from core.entities.veredict import Veredict

@dataclass
class RetrievedNews:
    """Entidad RetrievedNews - datos recuperados de medios de comunicación"""
    corpus: str
    title: str
    subtitle: str
    url:str
    published: datetime
    source: KnowledgeSource
    def __init__(self,corpus:str, title:str,subtitle:str,url:str,source:KnowledgeSource):
        self.corpus = corpus
        self.url = url
        self.title = title
        self.subtitle =  subtitle
        self.source = source
