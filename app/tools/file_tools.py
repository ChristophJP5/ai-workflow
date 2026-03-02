#!/usr/bin/env python3
"""
File Tools - Read, write, and edit project files.
"""

import asyncio
from pathlib import Path
from typing import Optional, Union


class FileTools:
    """
    Tools for file operations.
    """

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize file tools.

        Args:
            base_path: Base path for file operations (optional)
        """
        self.base_path = Path(base_path) if base_path else None

    async def read(self, filepath: str) -> str:
        """
        Read file contents.

        Args:
            filepath: Path to the file

        Returns:
            File contents as string
        """
        path = self._resolve_path(filepath)
        await self._log_operation("read", filepath)
        
        # Simulate async file read
        await asyncio.sleep(0.01)
        
        if path.exists():
            return path.read_text(encoding='utf-8')
        else:
            raise FileNotFoundError(f"File not found: {filepath}")

    async def write(self, filepath: str, content: str) -> bool:
        """
        Write content to a file.

        Args:
            filepath: Path to the file
            content: Content to write

        Returns:
            True if successful
        """
        path = self._resolve_path(filepath)
        await self._log_operation("write", filepath)
        
        # Simulate async file write
        await asyncio.sleep(0.01)
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return True

    async def edit(self, filepath: str, old_text: str, new_text: str) -> bool:
        """
        Edit file by replacing text.

        Args:
            filepath: Path to the file
            old_text: Text to find and replace
            new_text: Replacement text

        Returns:
            True if successful
        """
        path = self._resolve_path(filepath)
        await self._log_operation("edit", filepath)
        
        # Simulate async operation
        await asyncio.sleep(0.01)
        
        if path.exists():
            content = path.read_text(encoding='utf-8')
            if old_text in content:
                new_content = content.replace(old_text, new_text)
                path.write_text(new_content, encoding='utf-8')
                return True
            else:
                raise ValueError(f"Text not found in file: {filepath}")
        else:
            raise FileNotFoundError(f"File not found: {filepath}")

    def _resolve_path(self, filepath: str) -> Path:
        """Resolve filepath against base_path if set."""
        path = Path(filepath)
        if self.base_path and not path.is_absolute():
            path = self.base_path / path
        return path

    async def _log_operation(self, operation: str, filepath: str):
        """Log file operation (placeholder)."""
        print(f"   📁 File {operation}: {filepath}")

    async def exists(self, filepath: str) -> bool:
        """Check if file exists."""
        path = self._resolve_path(filepath)
        return path.exists()

    async def list_files(self, directory: str = ".") -> list:
        """List files in directory."""
        path = self._resolve_path(directory)
        if path.exists() and path.is_dir():
            return [str(p) for p in path.iterdir()]
        return []
