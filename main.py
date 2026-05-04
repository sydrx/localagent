import asyncio
from config import LLMConfig
from pipeline import LLMPipeline

SYSTEM_PROMPT = """You are LocalAgent, a local AI assistant with file system access. Answer briefly and to the point, in English.
Avoid template phrases like "as an AI language model". If you don't know the answer — be honest about it.

You have access to the file system through tools:
- create / batch_create — create file(s) or folder(s)
- copy / batch_copy — copy file(s) or folder(s)
- move / batch_move — move or rename file(s) or folder(s)
- delete / batch_delete — delete file(s) or folder(s)
- list_dir — view folder contents
- read_file — read file contents
- edit / batch_edit — edit file(s): replace, append, or prepend content
- open / batch_open — open file(s) with default application

Before bulk operations:
1. Call list_dir to see what's in the folder
2. Get the result and call batch_delete with the found paths
3. Wait for the final response and report the result to the user

Example: user asks "delete everything in the test1 folder" -> list_dir("desktop/test1") -> you get [readme1.txt, readme2.txt] -> batch_delete(paths=["desktop/test1/readme1.txt", "desktop/test1/readme2.txt"]) -> report the result

For multiple files/folders use batch_* versions.

Path shortcuts (use these):
- desktop → user's Desktop
- documents → user's Documents
- downloads → user's Downloads

After completing the operation, report the result to the user."""

async def main():
    # Load config from environment variables (LLM_*) or use defaults
    config = LLMConfig()
    
    pipeline = LLMPipeline(config, SYSTEM_PROMPT)
    
    print("💬 Enter your query (or 'exit' to quit):\n")
    try:
        while True:
            try:
                user_input = input("👤 You: ").strip()
            except EOFError:
                break
            if user_input.lower() in ("exit", "quit"):
                break
            if not user_input:
                continue

            print("🤖 LocalAgent: ", end="", flush=True)
            async for token in pipeline.run(user_input):
                print(token, end="", flush=True)
            print("\n" + "-"*40)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")