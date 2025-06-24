from core.interfaces.i_LLM import i_LLM
from google import genai
from google.genai import types

class GemmaLLM(i_LLM):
    api_key:str
    model:str
    def __init__(self,api_key,model):
        self.api_key = api_key
        self.model = model

    def ask_model(self,sytem_message,user_message) -> str:
        """LLamar a un modelo,  y que responde"""
        client = genai.Client(api_key=self.api_key)
        contents = [
            types.Content(
                role="model",
                parts=[
                    types.Part.from_text(text=sytem_message),
                ],
            ),
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=user_message),
                ],
            ),
        ]
        response=[]
        generate_content_config = types.GenerateContentConfig(max_output_tokens=2000,response_mime_type="text/plain",)
        for chunk in client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=generate_content_config,
        ):
            response.append(chunk.text)
        return " ".join(response)
