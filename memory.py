from typing import List, Dict
from config import LLMConfig

class ConversationMemory:
    def __init__(self, config: LLMConfig):
        self.config = config
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        self._trim_context()

    def get_messages(self) -> List[Dict[str, str]]:
        return self.history.copy()

    def _trim_context(self):
        # Simple sliding window: keep the last N messages
        # For precise token control, tiktoken can be integrated
        while len(self.history) > 6:
            self.history.pop(0)