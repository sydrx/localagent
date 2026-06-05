import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List

def _resolve_path(path: str) -> str:
    """Expands shortcuts to full paths. Supports composite paths: desktop/folder/file"""
    home = Path.home()
    shortcuts = {
        "desktop": str(home / "Desktop"),
        "documents": str(home / "Documents"),
        "downloads": str(home / "Downloads"),
    }

    path = path.strip()

    # Replace ~ with home directory
    if path.startswith("~"):
        return str(home) + path[1:]

    # Check shortcuts (including composite paths)
    path_lower = path.lower()
    for shortcut, full_path in shortcuts.items():
        if path_lower == shortcut:
            return full_path
        if path_lower.startswith(shortcut + "/") or path_lower.startswith(shortcut + "\\"):
            # Replace shortcut with full path, keep the remainder
            remainder = path[len(shortcut):]
            return full_path + remainder

    return path

def create(path: str, name: str, item_type: str = "folder", content: str = "") -> Dict[str, str]:
    """Creates a file or folder
    item_type: 'file' | 'folder'
    content: file content (only if item_type='file')
    """
    try:
        resolved_path = _resolve_path(path)
        full_path = Path(resolved_path) / name

        if item_type == "folder":
            full_path.mkdir(parents=True, exist_ok=True)
            return {"status": "success", "path": str(full_path), "type": "folder"}
        elif item_type == "file":
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            return {"status": "success", "path": str(full_path), "type": "file"}
        else:
            return {"status": "error", "message": f"Unknown type: {item_type}. Use 'file' or 'folder'"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def copy(source: str, destination: str) -> Dict[str, str]:
    """Copies a file or folder"""
    try:
        src = Path(_resolve_path(source))
        dst = Path(_resolve_path(destination))

        if not src.exists():
            return {"status": "error", "message": f"Source not found: {source}"}

        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        else:
            shutil.copytree(src, dst, dirs_exist_ok=True)

        return {"status": "success", "source": str(src), "destination": str(dst)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def move(source: str, destination: str) -> Dict[str, str]:
    """Moves a file or folder"""
    try:
        src = Path(_resolve_path(source))
        dst = Path(_resolve_path(destination))

        if not src.exists():
            return {"status": "error", "message": f"Source not found: {source}"}

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

        return {"status": "success", "source": str(src), "destination": str(dst)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete(path: str) -> Dict[str, str]:
    """Deletes a file or folder"""
    try:
        target = Path(_resolve_path(path))

        if not target.exists():
            return {"status": "error", "message": f"Not found: {path}"}

        if target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)

        return {"status": "success", "deleted": str(target)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def batch_create(items: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Batch creation of files and folders
    items: list of objects with fields {path, name, item_type, content}
    """
    results = []
    for item in items:
        try:
            result = create(
                path=item.get("path", ""),
                name=item.get("name", ""),
                item_type=item.get("item_type", "folder"),
                content=item.get("content", "")
            )
            results.append(result)
        except Exception as e:
            results.append({"status": "error", "message": str(e), "item": item})
    return {"status": "success", "results": results}

def batch_copy(items: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Batch copying of files and folders
    items: list of objects with fields {source, destination}
    """
    results = []
    for item in items:
        try:
            result = copy(
                source=item.get("source", ""),
                destination=item.get("destination", "")
            )
            results.append(result)
        except Exception as e:
            results.append({"status": "error", "message": str(e), "item": item})
    return {"status": "success", "results": results}

def batch_move(items: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Batch moving of files and folders
    items: list of objects with fields {source, destination}
    """
    results = []
    for item in items:
        try:
            result = move(
                source=item.get("source", ""),
                destination=item.get("destination", "")
            )
            results.append(result)
        except Exception as e:
            results.append({"status": "error", "message": str(e), "item": item})
    return {"status": "success", "results": results}

def batch_delete(paths: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """Batch deletion of files and folders
    paths: list of paths to delete
    """
    results = []
    for path in paths:
        try:
            result = delete(path)
            results.append(result)
        except Exception as e:
            results.append({"status": "error", "message": str(e), "path": path})
    return {"status": "success", "results": results}

def list_dir(path: str) -> Dict[str, Any]:
    """Shows folder contents: files and subfolders"""
    try:
        target = Path(_resolve_path(path))
        if not target.exists():
            return {"status": "error", "message": f"Not found: {path}"}
        if not target.is_dir():
            return {"status": "error", "message": f"Not a directory: {path}"}

        items = []
        for item in target.iterdir():
            items.append({
                "name": item.name,
                "type": "folder" if item.is_dir() else "file",
                "path": str(item)
            })

        return {"status": "success", "path": str(target), "items": items}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def read_file(path: str) -> Dict[str, str]:
    """Reads the contents of a text file"""
    try:
        target = Path(_resolve_path(path))
        if not target.exists():
            return {"status": "error", "message": f"Not found: {path}"}
        if not target.is_file():
            return {"status": "error", "message": f"Not a file: {path}"}

        content = target.read_text(encoding="utf-8")
        return {"status": "success", "path": str(target), "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def edit(path: str, content: str, mode: str = "replace") -> Dict[str, str]:
    """Edits an existing file
    mode: 'replace' | 'append' | 'prepend' — how to modify the file
    """
    try:
        target = Path(_resolve_path(path))
        if not target.exists():
            return {"status": "error", "message": f"File not found: {path}"}
        if not target.is_file():
            return {"status": "error", "message": f"Not a file: {path}"}

        if mode == "replace":
            target.write_text(content, encoding="utf-8")
        elif mode == "append":
            with open(target, "a", encoding="utf-8") as f:
                f.write(content)
        elif mode == "prepend":
            original = target.read_text(encoding="utf-8")
            target.write_text(content + original, encoding="utf-8")
        else:
            return {"status": "error", "message": f"Unknown mode: {mode}. Use 'replace', 'append', or 'prepend'"}

        return {"status": "success", "path": str(target), "mode": mode}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def open_file(path: str) -> Dict[str, str]:
    """Opens a file with the default application"""
    try:
        target = Path(_resolve_path(path))
        if not target.exists():
            return {"status": "error", "message": f"Not found: {path}"}

        abs_path = str(target.resolve())

        if os.name == 'nt':  # Windows
            os.startfile(abs_path)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.run(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', abs_path], check=True)

        return {"status": "success", "path": abs_path, "action": "opened"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def batch_edit(items: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Batch editing of files
    items: list of objects with fields {path, content, mode}
    """
    results = []
    for item in items:
        try:
            result = edit(
                path=item.get("path", ""),
                content=item.get("content", ""),
                mode=item.get("mode", "replace")
            )
            results.append(result)
        except Exception as e:
            results.append({"status": "error", "message": str(e), "item": item})
    return {"status": "success", "results": results}


def batch_open(paths: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """Batch opening of files
    paths: list of paths to open
    """
    results = []
    for path in paths:
        try:
            result = open_file(path)
            results.append(result)
        except Exception as e:
            results.append({"status": "error", "message": str(e), "path": path})
    return {"status": "success", "results": results}


def run_command(command: str, cwd: str = None, timeout: int = 30) -> Dict[str, Any]:
    """Executes a shell command and returns the result
    command: the command to execute (e.g., 'pip install requests' or 'python script.py')
    cwd: working directory (if None, uses current directory or resolves if it's a shortcut)
    timeout: maximum time to wait in seconds (default 30)
    
    v1.2.1: Auto-resolve relative paths in commands, better error handling
    """
    try:
        # Resolve working directory if provided
        resolved_cwd = None
        if cwd:
            resolved_cwd = _resolve_path(cwd)
        
        # Try to auto-resolve relative paths in the command if cwd is not provided
        # This helps when users specify paths like 'desktop/script.py'
        if not cwd and ("/" in command or "\\" in command):
            # Check if command starts with a path-like pattern
            parts = command.split(" ")
            if len(parts) > 0:
                first_part = parts[0]
                # Check if first part looks like a relative path
                if (first_part.startswith("desktop") or first_part.startswith("documents") or 
                    first_part.startswith("downloads")):
                    # Try to resolve it
                    resolved_path = _resolve_path(first_part)
                    if Path(resolved_path).exists():
                        # Replace the relative path with absolute path (with quotes if contains spaces)
                        if " " in resolved_path:
                            command = command.replace(first_part, f'"{resolved_path}"', 1)
                        else:
                            command = command.replace(first_part, resolved_path, 1)
        
        # Use shell=True to support complex commands, pipes, etc.
        result = subprocess.run(
            command,
            shell=True,
            cwd=resolved_cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "status": "success",
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output": result.stdout if result.returncode == 0 else result.stderr,
            "cwd": resolved_cwd
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": f"Command timed out after {timeout} seconds",
            "command": command,
            "cwd": resolved_cwd
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "command": command,
            "cwd": resolved_cwd
        }


def run_script(path: str, args: str = "", timeout: int = 60) -> Dict[str, Any]:
    """Runs a Python script or other executable file
    path: path to the script/executable
    args: command line arguments to pass to the script (e.g., "arg1 arg2")
    timeout: maximum time to wait in seconds (default 60)
    """
    try:
        target = Path(_resolve_path(path))
        
        if not target.exists():
            return {"status": "error", "message": f"File not found: {path}"}
        
        if not target.is_file():
            return {"status": "error", "message": f"Not a file: {path}"}
        
        # Build command based on file extension
        abs_path = str(target.resolve())
        file_ext = target.suffix.lower()
        
        if file_ext == ".py":
            # Python script
            command = f'python "{abs_path}"'
        elif file_ext in [".ps1"]:
            # PowerShell script
            command = f'powershell -ExecutionPolicy Bypass -File "{abs_path}"'
        elif file_ext in [".bat", ".cmd"]:
            # Batch file
            command = f'"{abs_path}"'
        elif file_ext in [".exe"]:
            # Executable
            command = f'"{abs_path}"'
        else:
            # Try to execute directly
            command = f'"{abs_path}"'
        
        # Add arguments if provided
        if args:
            command += f' {args}'
        
        # Execute
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(target.parent)
        )
        
        return {
            "status": "success",
            "script": str(target),
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output": result.stdout if result.returncode == 0 else result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": f"Script timed out after {timeout} seconds",
            "script": path
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "script": path
        }