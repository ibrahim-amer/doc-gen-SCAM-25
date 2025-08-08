from tinaa.doc_gen.config.BaseLLM import BaseLLM
class OpenAILLM(BaseLLM):
    def __init__(self, api_key: str, model_name: str = 'gpt-4o', temperature: float = 0.3):
        import openai
        openai.api_key = api_key
        self.temperature = temperature
        self.client = openai
        self.model_name = model_name

    def generate(self, messages: list[str], temperature: float = 0.3) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature
        )
        return response.choices[0].message.content
