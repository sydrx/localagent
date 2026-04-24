from typing import Optional

class PromptTemplate:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    def format(self, user_input: str, memory_messages: list) -> list:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(memory_messages)
        messages.append({"role": "user", "content": user_input})
        return messages