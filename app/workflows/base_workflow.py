#!/usr/bin/env python3
"""
Base Workflow - Abstract base class for all workflows.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
import uuid

from logging.workflow_logger import WorkflowLogger


class BaseWorkflow(ABC):
    """
    Abstract base class for all workflows.
    Provides common functionality for logging and state management.
    """

    def __init__(self, name: str):
        """
        Initialize the workflow.

        Args:
            name: Name of the workflow
        """
        self.name = name
        self.workflow_id = str(uuid.uuid4())[:8]
        self.logger = WorkflowLogger()
        self.state = {}
        self.start_time = None

    async def execute(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the workflow.

        Args:
            classification: Task classification from the agent

        Returns:
            Workflow execution result
        """
        self.start_time = datetime.now()
        await self.logger.log_workflow_start(
            self.workflow_id,
            self.name,
            classification
        )

        try:
            result = await self._run_workflow(classification)
            await self.logger.log_workflow_complete(
                self.workflow_id,
                "success",
                result
            )
            return result
        except Exception as e:
            await self.logger.log_workflow_complete(
                self.workflow_id,
                "failed",
                {"error": str(e)}
            )
            raise

    @abstractmethod
    async def _run_workflow(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement the specific workflow logic.

        Args:
            classification: Task classification

        Returns:
            Workflow result
        """
        pass

    async def _collect_context(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect project context (to be implemented by subclasses).

        Args:
            classification: Task classification

        Returns:
            Context dictionary
        """
        return {}

    async def _generate_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate execution plan (to be implemented by subclasses).

        Args:
            context: Project context

        Returns:
            Execution plan
        """
        return {}

    async def _execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the plan (to be implemented by subclasses).

        Args:
            plan: Execution plan

        Returns:
            Execution results
        """
        return {}

    async def _validate_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate execution results (to be implemented by subclasses).

        Args:
            results: Execution results

        Returns:
            Validation results
        """
        return {"success": True}
