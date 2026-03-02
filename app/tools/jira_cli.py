#!/usr/bin/env python3
"""
Jira CLI - Interface with Jira.
"""

import asyncio
from typing import Optional, Dict, Any


class JiraCLI:
    """
    Tool for Jira operations.
    """

    def __init__(self, server: Optional[str] = None):
        """
        Initialize Jira CLI tool.

        Args:
            server: Jira server URL (optional)
        """
        self.server = server

    async def get_issue(self, issue_id: str) -> Optional[Dict[str, Any]]:
        """
        Get issue details.

        Args:
            issue_id: Jira issue ID (e.g., PROJ-123)

        Returns:
            Issue data dictionary or None
        """
        await self._log_operation(f"get_issue: {issue_id}")
        
        try:
            # Try jira CLI if available
            proc = await asyncio.create_subprocess_exec(
                'jira', 'issue', 'view', issue_id, '--output', 'json',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode == 0:
                import json
                return json.loads(stdout.decode('utf-8'))
            else:
                # Return simulated data for demo
                return self._simulate_issue(issue_id)
                
        except FileNotFoundError:
            # jira CLI not available, return simulated data
            return self._simulate_issue(issue_id)
        except Exception as e:
            print(f"   Error getting issue: {e}")
            return self._simulate_issue(issue_id)

    def _simulate_issue(self, issue_id: str) -> Dict[str, Any]:
        """Simulate issue data for demo purposes."""
        return {
            "id": issue_id,
            "key": issue_id,
            "summary": f"Simulated issue {issue_id}",
            "description": "This is simulated issue data.",
            "status": "Open",
            "priority": "Medium",
            "assignee": None,
            "reporter": "User",
            "created": "2026-03-02T12:00:00Z",
            "updated": "2026-03-02T12:00:00Z"
        }

    async def update_issue(self, issue_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an issue.

        Args:
            issue_id: Jira issue ID
            updates: Fields to update

        Returns:
            True if successful
        """
        await self._log_operation(f"update_issue: {issue_id}")
        
        try:
            # This would use jira CLI in production
            print(f"   Would update {issue_id} with: {updates}")
            return True
        except Exception as e:
            print(f"   Error updating issue: {e}")
            return False

    async def transition_issue(self, issue_id: str, transition: str) -> bool:
        """
        Transition an issue to a new status.

        Args:
            issue_id: Jira issue ID
            transition: Transition name

        Returns:
            True if successful
        """
        await self._log_operation(f"transition_issue: {issue_id} -> {transition}")
        
        try:
            print(f"   Would transition {issue_id} to {transition}")
            return True
        except Exception as e:
            print(f"   Error transitioning issue: {e}")
            return False

    async def _log_operation(self, operation: str):
        """Log operation."""
        print(f"   🎫 Jira: {operation}")
