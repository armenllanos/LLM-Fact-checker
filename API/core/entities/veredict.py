from dataclasses import dataclass
from typing import Optional
from datetime import datetime


class Veredict():
    """Veredictos"""

    TRUE_STATE:str = 'verdadero'
    FAKE_STATE:str =  'falso'
    NO_VALIDATION_STATE:str = 'no verificable'
    state:str
    
    def __init__(self, state:str):
        self.state = state

    def is_true(self):
        return self.state == self.TRUE_STATE
    def is_false(self):
        return self.state == self.FAKE_STATE
    def is_not_verified(self):
        return self.state == self.NO_VALIDATION_STATE
