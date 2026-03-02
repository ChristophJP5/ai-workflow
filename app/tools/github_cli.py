#!/usr/bin/env python3
"""
GitHub CLI - Interface with GitHub via CLI.
"""

import asyncio
import subprocess
from typing import Optional, Dict, Any


class GitHubCLI:
    """
    Tool for GitHub operations using gh CLI.
    """

    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize GitHub CLI tool.

        Args:
            repo_path: Path to the git repository
        """
        self.repo_path = repo_path

    async def get_status(self) -> Dict[str, Any]:
        """
        Get git repository status.

        Returns:
            Dictionary with git status information
        """
        await self._log_operation("status")
        
        try:
            # Simulate git status
            await asyncio.sleep(0.01)
            
            result = {
                "branch": "main",
                "ahead": 0,
                "behind": 0,
                "changes": False,
                "error": None
            }
            
            # Try to get actual git status if available
            try:
                proc = await asyncio.create_subprocess_exec(
                    'git', 'status', '--porcelain',
                    cwd=self.repo_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await proc.communicate()
                
                if proc.returncode == 0:
                    changes = stdout.decode('utf-8').strip()
                    result["changes"] = bool(changes)
                    
                    # Get current branch
                    proc_branch = await asyncio.create_subprocess_exec(
                        'git', 'branch', '--show-current',
                        cwd=self.repo_path,
                        stdout=asyncio.subprocess.PIPE
                    )
                    stdout, _ = await proc_branch.communicate()
                    if stdout:
                        result["branch"] = stdout.decode('utf-8').strip()
                        
            except Exception as e:
                result["error"] = str(e)
                result["simulated"] = True
                
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "simulated": True
            }

    async def create_branch(self, branch_name: str, base: str = "main") -> bool:
        """
        Create a new branch.

        Args:
            branch_name: Name of the new branch
            base: Base branch name

        Returns:
            True if successful
        """
        await self._log_operation(f"create_branch: {branch_name}")
        
        try:
            proc = await asyncio.create_subprocess_exec(
                'git', 'checkout', '-b', branch_name, base,
                cwd=self.repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                raise RuntimeError(stderr.decode('utf-8'))
                
            return True
            
        except Exception as e:
            print(f"   Error creating branch: {e}")
            return False

    async def commit(self, message: str, files: Optional[list] = None) -> bool:
        """
        Commit changes.

        Args:
            message: Commit message
            files: List of files to commit (optional)

        Returns:
            True if successful
        """
        await self._log_operation(f"commit: {message[:50]}")
        
        try:
            # Add files
            if files:
                for file in files:
                    proc = await asyncio.create_subprocess_exec(
                        'git', 'add', file,
                        cwd=self.repo_path
                    )
                    await proc.communicate()
            else:
                proc = await asyncio.create_subprocess_exec(
                    'git', 'add', '-A',
                    cwd=self.repo_path
                )
                await proc.communicate()
            
            # Commit
            proc = await asyncio.create_subprocess_exec(
                'git', 'commit', '-m', message,
                cwd=self.repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                raise RuntimeError(stderr.decode('utf-8'))
                
            return True
            
        except Exception as e:
            print(f"   Error committing: {e}")
            return False

    async def create_pr(self, title: str, body: str = "", base: str = "main") -> Optional[str]:
        """
        Create a pull request.

        Args:
            title: PR title
            body: PR description
            base: Base branch

        Returns:
            PR URL if successful
        """
        await self._log_operation(f"create_pr: {title}")
        
        try:
            # Use gh CLI if available
            cmd = ['gh', 'pr', 'create', '--title', title, '--base', base]
            if body:
                cmd.extend(['--body', body])
                
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=self.repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode == 0:
                return stdout.decode('utf-8').strip()
            else:
                raise RuntimeError(stderr.decode('utf-8'))
                
        except Exception as e:
            print(f"   Error creating PR: {e}")
            return None

    async def _log_operation(self, operation: str):
        """Log operation."""
        print(f"   🔧 GitHub: {operation}")
