# LocalAgent

[![Version](https://img.shields.io/badge/version-1.1.0-blue)](https://github.com/sydrx/localagent)

Local AI assistant with file system access. Works via LM Studio API with tool calling support.

## Features

- **💬 Chat with local LLM** — chat with the model through the console
- **📁 File operations** — create, copy, move and delete files and folders
- **📂 View contents** — see what's inside folders before operations
- **🚀 Batch operations** — perform bulk actions on multiple files
- **🏠 Smart paths** — use shortcuts like `desktop`, `documents`, `downloads`

## Tools

| Tool | Description |
|------------|----------|
| `create` / `batch_create` | Create file(s) or folder(s) |
| `copy` / `batch_copy` | Copy file(s) or folder(s) |
| `move` / `batch_move` | Move or rename |
| `delete` / `batch_delete` | Delete file(s) or folder(s) |
| `list_dir` | View folder contents |
| `read_file` | Read file contents |
| `edit` / `batch_edit` | Edit file(s): replace, append, or prepend content |
| `open` / `batch_open` | Open file(s) with default application |

## Path shortcuts

- `desktop` → `C:\Users\<username>\Desktop`
- `documents` → `C:\Users\<username>\Documents`
- `downloads` → `C:\Users\<username>\Downloads`

## Requirements

1. **LM Studio** with a running local server (default `http://localhost:1234`)
2. **Python 3.10+**
3. **OpenAI SDK** (`pip install openai`)

## Installation

```bash
git clone https://github.com/sydrx/localagent.git
cd localagent
pip install openai
```

## Launch

1. Launch LM Studio and enable the local server (port 1234)
2. Load a model with tool calling support (e.g., `qwen/qwen3-8b`)
3. Run the agent:

```bash
python main.py
```

## Usage examples

```
💬 Enter your query (or 'exit' to quit):

👤 You: create three folders on the desktop: test1, test2, test3
🤖 LocalAgent: Created three folders on the desktop.
----------------------------------------
👤 You: what's inside test1?
🤖 LocalAgent: Inside test1 folder: readme.txt, data.json
----------------------------------------
👤 You: delete everything in the test1 folder
🤖 LocalAgent: Deleted readme.txt and data.json from the test1 folder.
----------------------------------------
👤 You: add "Hello World" to the end of readme.txt
🤖 LocalAgent: Appended text to readme.txt.
----------------------------------------
👤 You: open test1/data.json
🤖 LocalAgent: Opened data.json with the default application.
----------------------------------------
👤 You: exit
👋 Goodbye!
```

## Architecture

```
main.py          — CLI interface
pipeline.py      — ReAct request processing loop
client.py        — OpenAI client for LM Studio
config.py        — Model configuration
memory.py        — Message history
prompt.py        — Prompt formatting
tools/fs_tools.py — File system tools
```

## License

MIT
