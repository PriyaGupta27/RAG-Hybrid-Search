from langchain_ollama import ChatOllama
from app.config.settings import settings

class LLM:
    def __init__(self):
        self.model = ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            temperature=0,
        )

    def generate( self, prompt: str):
        response = self.model.invoke(prompt)
        return response.content

    def stream(self, prompt: str):
        for chunk in self.model.stream(prompt):
            if chunk.content:
                yield chunk.content