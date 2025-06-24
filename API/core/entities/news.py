from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from core.entities.claim import Claim
from core.entities.veredict import Veredict

@dataclass
class News:
    """Entidad News - Reglas de negocio centrales"""
    id: Optional[int]
    text: str
    content_veredict: Veredict
    semantic_veredict: Veredict
    content_score: float
    semantic_score: float
    general_veredict:Veredict
    claims: list[Claim]
    
    def __init__(self,text,semantic_veredict, semantic_score,content_veredict,content_score):
        self.text= text
        self.semantic_veredict = semantic_veredict
        self.semantic_score = semantic_score
        self.content_veredict = content_veredict
        self.content_score = content_score