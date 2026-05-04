import json
from config import LLMConfig
from client import LMStudioClient
from memory import ConversationMemory
from prompt import PromptTemplate
from typing import AsyncIterator
from tools.fs_tools import (create, copy, move, delete, batch_create, batch_copy, batch_move, batch_delete, list_dir, read_file, edit, open_file, batch_edit, batch_open)

class LLMPipeline:
    def __init__(self, config: LLMConfig, system_prompt: str):
        self.config = config
        self.client = LMStudioClient(config)
        self.memory = ConversationMemory(config)
        self.prompt = PromptTemplate(system_prompt)

    def _execute_tool(self, tool_name: str, arguments: str) -> str:
        """Executes the tool and returns the result as a string"""
        try:
            args = json.loads(arguments)
            if tool_name == "create":
                result = create(**args)
            elif tool_name == "batch_create":
                result = batch_create(**args)
            elif tool_name == "copy":
                result = copy(**args)
            elif tool_name == "batch_copy":
                result = batch_copy(**args)
            elif tool_name == "move":
                result = move(**args)
            elif tool_name == "batch_move":
                result = batch_move(**args)
            elif tool_name == "delete":
                result = delete(**args)
            elif tool_name == "batch_delete":
                result = batch_delete(**args)
            elif tool_name == "list_dir":
                result = list_dir(**args)
            elif tool_name == "read_file":
                result = read_file(**args)
            elif tool_name == "edit":
                result = edit(**args)
            elif tool_name == "open":
                result = open_file(**args)
            elif tool_name == "batch_edit":
                result = batch_edit(**args)
            elif tool_name == "batch_open":
                result = batch_open(**args)
            else:
                return json.dumps({"error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)

    async def run(self, user_input: str) -> AsyncIterator[str]:
        messages = self.prompt.format(user_input, self.memory.get_messages())
        
        # First call with tools
        response_msg = await self.client.chat_completion_with_tools(messages)
        
        # Processing tool call chain (ReAct loop)
        while response_msg.tool_calls:
            print(f"\n[DEBUG] Processing {len(response_msg.tool_calls)} tool call(s)")
            
            # Add model response with tool_calls to history
            messages.append({
                "role": "assistant",
                "content": response_msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in response_msg.tool_calls
                ]
            })
            
            # Execute each tool and add results
            for tool in response_msg.tool_calls:
                result = self._execute_tool(tool.function.name, tool.function.arguments)
                print(f"\n[TOOL] {tool.function.name}({tool.function.arguments}) -> {result[:200]}...")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool.id,
                    "content": result
                })
            
            # Get the next response (could be another tool_call or final text)
            response_msg = await self.client.chat_completion_with_tools(messages)
        
        # Return the final answer (content may be None)
        content = response_msg.content or ""
        for char in content:
            yield char
        
        # Save to memory
        self.memory.add_message("user", user_input)
        self.memory.add_message("assistant", content)