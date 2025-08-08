from tinaa.doc_gen.config.config import Config
from tinaa.doc_gen.config.BaseLLM import BaseLLM
from tinaa.doc_gen.config.OpenAILLM import OpenAILLM
from tinaa.doc_gen.config.GeminiLLM import GeminiLLM
from tinaa.doc_gen.config.TelusLLM import TelusLLM
from tinaa.doc_gen.config.LLMProvider import LLMProvider
from tinaa.doc_gen.config.TelusFuelIXLLM import TelusFuelIXLLM  # ⬅️ import the new class


class LLMFactory:
    @staticmethod
    def from_config(config: Config, provider: LLMProvider) -> BaseLLM:
        if provider == LLMProvider.OPENAI:
            return OpenAILLM(
                api_key=config.OPENAI.API_KEY,
                model_name=config.OPENAI.MODEL,
                temperature=config.OPENAI.TEMPERATURE
            )
        elif provider == LLMProvider.GEMINI:
            return GeminiLLM(
                api_key=config.GEMINI.KEY,
                model_name=config.GEMINI.MODEL,
                temperature=config.GEMINI.TEMPERATURE
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")