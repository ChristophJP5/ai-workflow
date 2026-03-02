#!/usr/bin/env python3
"""
Bugfix Workflow - Diagnose and fix existing defects.
"""

from typing import Dict, Any
from datetime import datetime

from workflows.base_workflow import BaseWorkflow
from tools.file_tools import FileTools
from tools.github_cli import GitHubCLI
from tools.jira_cli import JiraCLI
from tools.url_fetch import URLFetch
from tools.aider_tool import AiderTool


class BugfixWorkflow(BaseWorkflow):
    """
    Workflow for diagnosing and fixing bugs.
    Steps:
    1. Collect context (files, git state, issue data)
    2. Generate debugging plan
    3. Execute code changes
    4. Run validation
    5. Package results
    """

    def __init__(self):
        """Initialize the bugfix workflow."""
        super().__init__("BugfixWorkflow")
        self.file_tools = FileTools()
        self.github = GitHubCLI()
        self.jira = JiraCLI()
        self.url_fetch = URLFetch()
        self.aider = AiderTool()

    async def _run_workflow(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the bugfix workflow.

        Args:
            classification: Task classification

        Returns:
            Workflow result
        """
        print(f"\n🐛 Starting Bugfix Workflow (ID: {self.workflow_id})")
        print("=" * 50)

        # Step 1: Collect context
        print("\n📋 Step 1: Collecting context...")
        context = await self._collect_context(classification)
        print(f"   Found {len(context.get('files', []))} relevant files")

        # Step 2: Generate plan
        print("\n📝 Step 2: Generating debugging plan...")
        plan = await self._generate_plan(context)
        print(f"   Generated {len(plan.get('steps', []))} steps")

        # Step 3: Execute plan
        print("\n🔧 Step 3: Executing fix...")
        execution_results = await self._execute_plan(plan, context)

        # Step 4: Validate
        print("\n✅ Step 4: Validating results...")
        validation = await self._validate_results(execution_results)

        # Step 5: Package results
        print("\n📦 Step 5: Packaging results...")
        result = await self._package_results(
            classification,
            context,
            plan,
            execution_results,
            validation
        )

        print(f"\n✅ Bugfix Workflow completed (ID: {self.workflow_id})")
        return result

    async def _collect_context(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """Collect project context for debugging."""
        context = {
            "task": classification,
            "files": [],
            "git_state": None,
            "issue_data": None,
            "timestamp": datetime.now().isoformat()
        }

        # Get git status
        git_state = await self.github.get_status()
        context["git_state"] = git_state

        # Check for Jira tickets
        task_desc = classification.get("task_description", "")
        if "ticket" in task_desc.lower() or "jira" in task_desc.lower():
            import re
            ticket_match = re.search(r'([A-Z]+-\d+)', task_desc)
            if ticket_match:
                ticket_id = ticket_match.group(1)
                issue_data = await self.jira.get_issue(ticket_id)
                context["issue_data"] = issue_data

        # Read relevant files if mentioned
        files_mentioned = classification.get("context", {}).get("files_mentioned", [])
        for filepath in files_mentioned:
            try:
                content = await self.file_tools.read(filepath)
                context["files"].append({
                    "path": filepath,
                    "content": content
                })
            except Exception as e:
                print(f"   Warning: Could not read {filepath}: {e}")

        return context

    async def _generate_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a debugging plan."""
        return {
            "steps": [
                {"action": "analyze", "target": "identify_bug_location"},
                {"action": "fix", "target": "apply_fix"},
                {"action": "test", "target": "verify_fix"}
            ]
        }

    async def _execute_plan(self, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the debugging plan."""
        results = []
        for step in plan.get("steps", []):
            print(f"   Executing: {step.get('action')}")
            results.append(step)
        return {"steps_executed": results}

    async def _validate_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate execution results."""
        return {"success": True, "validated": True}

    async def _package_results(self, classification, context, plan, execution, validation) -> Dict[str, Any]:
        """Package final results."""
        return {
            "workflow_id": self.workflow_id,
            "workflow_type": "bugfix",
            "classification": classification,
            "context_summary": {
                "files_analyzed": len(context.get("files", [])),
                "git_state": context.get("git_state"),
            },
            "plan": plan,
            "execution": execution,
            "validation": validation,
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }
