# LocalAgent

[![Version](https://img.shields.io/badge/version-1.2.1-blue)](https://github.com/sydrx/localagent)

Local AI assistant with file system access and terminal execution. Works via LM Studio API with tool calling support.

## Features

- **💬 Chat with local LLM** — chat with the model through the console
- **📁 File operations** — create, copy, move and delete files and folders
- **📂 View contents** — see what's inside folders before operations
- **🚀 Batch operations** — perform bulk actions on multiple files
- **🏠 Smart paths** — use shortcuts like `desktop`, `documents`, `downloads`
- **⌨️ Terminal execution** — run commands, scripts, and executables directly from the agent

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
| `run_command` | Execute shell commands (PowerShell/bash) |
| `run_script` | Run Python scripts, PowerShell scripts, batch files, or executables |

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

## Changelog

### v1.2.1 (Latest)
- **Improved path handling** — auto-resolve relative paths in `run_command` (e.g., `desktop/script.py`)
- **Better error tracking** — include `cwd` in response for debugging
- **Enhanced documentation** — examples of terminal usage

### v1.2.0
- Added terminal execution support (`run_command`, `run_script`)
- Support for Python, PowerShell, batch files, and executables
- Timeout control on command execution

### v1.1.0
- File system tools (create, copy, move, delete, edit)
- Batch operations for bulk file actions
- Smart path shortcuts (desktop, documents, downloads)

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
👤 You: install python requests library
🤖 LocalAgent: Successfully installed requests library via pip.
----------------------------------------
👤 You: show me Python version
🤖 LocalAgent: Python 3.10.5
----------------------------------------
👤 You: create a script that prints "Hello from Python" and run it
🤖 LocalAgent: Created hello_script.py and executed it. Output: Hello from Python
----------------------------------------
👤 You: exit
👋 Goodbye!
```

## Terminal Examples

The agent can now execute commands and scripts:

```
👤 You: run pip install numpy
🤖 LocalAgent: Successfully installed numpy.

👤 You: what python packages do I have installed?
🤖 LocalAgent: [Lists installed packages from pip list]

👤 You: create a python script on desktop that calculates fibonacci numbers and run it with argument 10
🤖 LocalAgent: Created and executed the script. Output: [fibonacci sequence up to 10]
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
