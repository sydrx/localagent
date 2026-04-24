import openai
import json
from typing import AsyncIterator, List, Dict, Optional, Any
from config import LLMConfig

def _batch_schemas() -> list:
    """Schemas for batch operations (bulk file actions)"""
    return [
        {
            "type": "function",
            "function": {
                "name": "batch_create",
                "description": "Batch creation of files and folders in a single call. Use for complex structures.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "description": "List of items to create",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string", "description": "Base path (desktop, documents, or path like 'desktop/test1')"},
                                    "name": {"type": "string", "description": "File or folder name"},
                                    "item_type": {"type": "string", "enum": ["file", "folder"], "description": "Type: 'file' or 'folder'"},
                                    "content": {"type": "string", "description": "File content", "default": ""}
                                },
                                "required": ["path", "name", "item_type"]
                            }
                        }
                    },
                    "required": ["items"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "batch_copy",
                "description": "Batch copy of files and folders in a single call.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "description": "List of copy operations",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "source": {"type": "string", "description": "Source path"},
                                    "destination": {"type": "string", "description": "Destination path"}
                                },
                                "required": ["source", "destination"]
                            }
                        }
                    },
                    "required": ["items"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "batch_move",
                "description": "Batch move of files and folders in a single call.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "description": "List of move operations",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "source": {"type": "string", "description": "Source path"},
                                    "destination": {"type": "string", "description": "Destination path"}
                                },
                                "required": ["source", "destination"]
                            }
                        }
                    },
                    "required": ["items"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "batch_delete",
                "description": "Batch deletion of files and folders in a single call. Careful!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "paths": {
                            "type": "array",
                            "description": "List of paths to delete",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["paths"]
                }
            }
        }
    ]

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "create",
            "description": "Create a single file or folder. For a file, use item_type='file' and pass content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Base path (desktop, documents, downloads, or full path)"},
                    "name": {"type": "string", "description": "File or folder name"},
                    "item_type": {"type": "string", "enum": ["file", "folder"], "description": "What to create: 'file' or 'folder'"},
                    "content": {"type": "string", "description": "File content (only for item_type='file')", "default": ""}
                },
                "required": ["path", "name", "item_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "copy",
            "description": "Copy a file or folder",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "Source path (file or folder)"},
                    "destination": {"type": "string", "description": "Destination path (where to copy)"}
                },
                "required": ["source", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move",
            "description": "Move or rename a file or folder",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "Source path"},
                    "destination": {"type": "string", "description": "Destination path (where to move)"}
                },
                "required": ["source", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete",
            "description": "Delete a file or folder recursively",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file or folder to delete"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "Show folder contents (files and subfolders)",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the folder (desktop, documents, or full path)"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a text file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file"}
                },
                "required": ["path"]
            }
        }
    }
]

class LMStudioClient:
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = openai.AsyncOpenAI(
            base_url=config.base_url,
            api_key=config.api_key
        )

    async def chat_completion_stream(
        self, messages: List[Dict[str, str]]
    ) -> AsyncIterator[str]:
        """Streaming chat without tools"""
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            top_p=self.config.top_p,
            stream=True,
        )
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def chat_completion_with_tools(
        self, messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Non-streaming chat with tool support"""
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            top_p=self.config.top_p,
            stream=False,
            tools=_batch_schemas() + TOOLS_SCHEMA,
            tool_choice="auto",
        )
        return response.choices[0].message