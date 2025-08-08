from tinaa.doc_gen.config.BaseLLM import BaseLLM
import google.generativeai as genai

class GeminiLLM(BaseLLM):
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash-latest", temperature: float = 0.3):
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, messages: list[dict]) -> str:
        # for model in genai.list_models():
        #     print(model.name)
        # Convert OpenAI-style messages to Gemini format (excluding 'system')
        gemini_messages = []
        for msg in messages:
            role = msg["role"]
            if role == "system":
                role = "user"  # Gemini doesn't support 'system' role
            gemini_messages.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        # All messages except the final one go into history
        chat = self.model.start_chat(
            history=gemini_messages[:-1]
        )

        # Send the final user message and return the response
        final_text = gemini_messages[-1]["parts"][0]["text"]

        response = chat.send_message(
            final_text,
            generation_config={"temperature": self.temperature}
        )

        return response.text