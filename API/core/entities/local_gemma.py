import json
import requests
from core.interfaces.i_LLM import i_LLM
from google import genai
from google.genai import types

class LocalGemmaLLM(i_LLM):
    model:str
    def __init__(self,api_url,model):
        self.model = model
        self.type = 'Local'
        self.api_url = api_url

    def ask_model(self,sytem_message,user_message) -> str:
        """LLamar a un modelo,  y que responde"""
        headers = {
                "Content-Type": "application/json"
            }
   
        body = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": sytem_message
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.0,
            "max_tokens": -1,
            "stream": False
        }
        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(body))
            response.raise_for_status()
            r = response.json()
            return r['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            print(f"Error en la llamada a la API: {e}")
            return None
        
