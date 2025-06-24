from dataclasses import dataclass
from typing import Optional
from datetime import datetime



from core.entities.veredict import Veredict

@dataclass
class Claim:
    text: str
    veredict: Veredict
    score:float

    def __init__(self,claim_text:str):
        self.text = claim_text
        
