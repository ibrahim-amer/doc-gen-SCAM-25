from __future__ import annotations
import os
import yaml
from yaml import CLoader
from dataclasses import dataclass, field, asdict
from tinaa.doc_gen.config.LLMProvider import LLMProvider



@dataclass
class GeminiConfig:
    KEY: str = ""
    MODEL: str = "gemini-1.5-flash-latest"
    TEMPERATURE: float = 0.3

@dataclass
class OpenAIConfig:
    API_KEY: str = ""
    MODEL: str = "gpt-4o"
    TEMPERATURE: float = 0.3

@dataclass
class TelusConfig:
    API_KEY: str = ""
    BASE_URL: str = ""
    MODEL_NAME: str = ""

@dataclass
class Config:
    LLM_PROVIDER: str = "openai"
    UNICORN_KEY: str = ""
    GEMINI: GeminiConfig = field(default_factory=GeminiConfig)
    OPENAI: OpenAIConfig = field(default_factory=OpenAIConfig)
    TELUS: TelusConfig = field(default_factory=TelusConfig)

    @classmethod
    def load_from_file(cls, file_name: str = "config.yaml") -> Config:
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)

        try:
            with open(file_path, "r") as file:
                config_data = yaml.load(file, Loader=CLoader) or {}
        except FileNotFoundError:
            print(f"[ERROR] File not found: {file_path}")
            return cls()

        return cls(
            LLM_PROVIDER=config_data.get("LLM_PROVIDER", "").lower() or "openai",
            UNICORN_KEY=config_data.get("UNICORN_KEY", "") or "",
            GEMINI=GeminiConfig(**(config_data.get("GEMINI", {}) or {})),
            OPENAI=OpenAIConfig(**(config_data.get("OPENAI", {}) or {})),
            TELUS=TelusConfig(**(config_data.get("TELUS", {}) or {})),
        )

    @property
    def provider_enum(self) -> LLMProvider:
        try:
            return LLMProvider(self.LLM_PROVIDER.lower())
        except ValueError:
            raise ValueError(f"Invalid LLM_PROVIDER: {self.LLM_PROVIDER}")

    def get_config(self) -> dict:
        return {
            "LLM_PROVIDER": self.LLM_PROVIDER,
            "UNICORN_KEY": self.UNICORN_KEY,
            "GEMINI": asdict(self.GEMINI),
            "OPENAI": asdict(self.OPENAI),
            "TelusFuelEX": asdict(self.TELUS)
        }

    def __str__(self) -> str:
        lines = [f"{k}: {v if v else '[EMPTY]'}" for k, v in self.get_config().items()]
        return "\n".join(lines)
