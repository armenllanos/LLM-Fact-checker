from core.interfaces import i_LLM
from mistralai import Mistral

class MistralLLM(i_LLM):
    api_key:str
    model:str
    def __init__(self,api_key,model):
        self.api_key = api_key
        self.model = model
        self.type = 'Mistral'
    
    def ask_model(self,sytem_message,user_message) -> str:
        """LLamar a un modelo,  y que responde"""
        client = Mistral(api_key=self.api_key)
        messages = [
            {
                "role": "system",
                "content": sytem_message,
        },
            {
                "role": "user",
                "content": user_message,
            },
        ]

        chat_response = client.chat.complete(model= self.model,messages=messages)
        return chat_response.choices[0].message.content