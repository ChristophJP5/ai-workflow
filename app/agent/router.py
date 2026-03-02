#!/usr/bin/env python3
"""
Workflow Router - Routes tasks to the appropriate workflow.
"""

from typing import Dict, Any
from workflows.bugfix_workflow import BugfixWorkflow
from workflows.feature_workflow import FeatureWorkflow


class WorkflowRouter:
    """
    Router that directs tasks to the correct workflow based on classification.
    """

    def __init__(self):
        """Initialize available workflows."""
        self.workflows = {
            "bugfix": BugfixWorkflow,
            "feature": FeatureWorkflow,
        }

    def get_workflow(self, task_type: str) -> Any:
        """
        Get the appropriate workflow for a task type.

        Args:
            task_type: The classification string (bugfix, feature)

        Returns:
            Workflow class instance
        """
        workflow_class = self.workflows.get(task_type)
        if workflow_class:
            return workflow_class()
        else:
            # Default to feature workflow if unknown
            return FeatureWorkflow()

    async def route(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a classified task to its workflow.

        Args:
            classification: The task classification dictionary

        Returns:
            Workflow execution result
        """
        task_type = classification.get("task_type", "unknown")
        task_description = classification.get("task_description", "")

        print(f"🔀 Routing to workflow: {task_type}")
        print(f"   Description: {task_description[:100]}...")

        workflow = self.get_workflow(task_type)
        result = await workflow.execute(classification)

        return result
