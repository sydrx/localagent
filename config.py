from pydantic import BaseModel, Field
from typing import Optional

class LLMConfig(BaseModel):
    base_url: str = "http://localhost:1234/v1"
    model: str = "qwen/qwen3-8b"
    api_key: str = "not-needed"  # LM Studio ignores the key
    temperature: float = 0.6
    max_tokens: int = 2048
    context_window: int = 4096  # Qwen3-8B officially ~32K, but we limit for stability
    top_p: float = 0.9
    stream: bool = True

    class Config:
        env_prefix = "LLM_"