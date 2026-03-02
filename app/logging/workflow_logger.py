#!/usr/bin/env python3
"""
Workflow Logger - Structured logging for workflow execution.
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class WorkflowLogger:
    """
    Logger for workflow execution tracking.
    """

    def __init__(self, log_dir: Optional[str] = None):
        """
        Initialize the workflow logger.

        Args:
            log_dir: Directory for log files
        """
        self.log_dir = Path(log_dir) if log_dir else Path("./logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.active_workflows = {}

    async def log_workflow_start(self, workflow_id: str, workflow_name: str, 
                                  context: Dict[str, Any]) -> None:
        """
        Log workflow start.

        Args:
            workflow_id: Unique workflow ID
            workflow_name: Name of the workflow
            context: Initial context
        """
        await self._write_log({
            "event": "workflow_start",
            "workflow_id": workflow_id,
            "workflow_name": workflow_name,
            "timestamp": datetime.now().isoformat(),
            "context": context
        })
        
        self.active_workflows[workflow_id] = {
            "start_time": datetime.now(),
            "name": workflow_name,
            "steps": []
        }

    async def log_step_start(self, workflow_id: str, step_name: str, 
                             step_data: Dict[str, Any]) -> None:
        """
        Log step start.

        Args:
            workflow_id: Workflow ID
            step_name: Name of the step
            step_data: Step data
        """
        await self._write_log({
            "event": "step_start",
            "workflow_id": workflow_id,
            "step_name": step_name,
            "timestamp": datetime.now().isoformat(),
            "data": step_data
        })

    async def log_step_complete(self, workflow_id: str, step_name: str,
                                result: Dict[str, Any]) -> None:
        """
        Log step completion.

        Args:
            workflow_id: Workflow ID
            step_name: Name of the step
            result: Step result
        """
        await self._write_log({
            "event": "step_complete",
            "workflow_id": workflow_id,
            "step_name": step_name,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
        
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]["steps"].append({
                "name": step_name,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })

    async def log_tool_execution(self, workflow_id: str, tool_name: str,
                                 action: str, result: Any) -> None:
        """
        Log tool execution.

        Args:
            workflow_id: Workflow ID
            tool_name: Name of the tool
            action: Action performed
            result: Tool result
        """
        await self._write_log({
            "event": "tool_execution",
            "workflow_id": workflow_id,
            "tool_name": tool_name,
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })

    async def log_workflow_complete(self, workflow_id: str, status: str,
                                    result: Dict[str, Any]) -> None:
        """
        Log workflow completion.

        Args:
            workflow_id: Workflow ID
            status: Final status (success/failed)
            result: Final result
        """
        workflow_data = self.active_workflows.pop(workflow_id, {})
        start_time = workflow_data.get("start_time")
        
        duration = None
        if start_time:
            duration = (datetime.now() - start_time).total_seconds()
        
        await self._write_log({
            "event": "workflow_complete",
            "workflow_id": workflow_id,
            "status": status,
            "duration_seconds": duration,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })

    async def log_error(self, workflow_id: str, error: str, 
                        step: Optional[str] = None) -> None:
        """
        Log an error.

        Args:
            workflow_id: Workflow ID
            error: Error message
            step: Step where error occurred (optional)
        """
        await self._write_log({
            "event": "error",
            "workflow_id": workflow_id,
            "step": step,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })

    async def _write_log(self, log_entry: Dict[str, Any]) -> None:
        """
        Write log entry to file.

        Args:
            log_entry: Log entry dictionary
        """
        # Write to daily log file
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"workflow-{date_str}.jsonl"
        
        try:
            async with asyncio.Lock():
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Error writing log: {e}")

    def get_workflow_summary(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get summary of a workflow execution.

        Args:
            workflow_id: Workflow ID

        Returns:
            Workflow summary or None
        """
        if workflow_id in self.active_workflows:
            data = self.active_workflows[workflow_id]
            return {
                "workflow_id": workflow_id,
                "name": data["name"],
                "start_time": data["start_time"].isoformat() if data["start_time"] else None,
                "steps_executed": len(data["steps"]),
                "status": "running"
            }
        return None
