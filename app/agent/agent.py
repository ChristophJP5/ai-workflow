#!/usr/bin/env python3
"""
LLM Agent - Core agent for understanding and classifying user requests.
"""

from typing import Dict, Any, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseLanguageModel


class LLMAgent:
    """
    Main LLM agent that interprets user requests and orchestrates workflows.
    """

    SYSTEM_PROMPT = """You are an AI development assistant. Your job is to:
1. Understand the user's request
2. Classify the task type (bugfix or feature)
3. Extract relevant context and details
4. Route to the appropriate workflow

Available task types:
- "bugfix": Fix an existing defect, error, or issue in the code
- "feature": Implement new functionality or capability

Respond with a JSON object containing:
{
    "task_type": "bugfix" | "feature",
    "task_description": "detailed description of what needs to be done",
    "confidence": 0.0-1.0,
    "context": {
        "files_mentioned": [],
        "ticket_references": [],
        "priority": "low" | "medium" | "high"
    }
}
"""

    def __init__(self, llm: BaseLanguageModel):
        """
        Initialize the agent with a language model.

        Args:
            llm: LangChain-compatible language model
        """
        self.llm = llm
        self.conversation_history = []

    async def classify_request(self, user_message: str) -> Dict[str, Any]:
        """
        Classify a user request and extract task details.

        Args:
            user_message: The user's natural language request

        Returns:
            Dictionary with task classification and details
        """
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=f"Classify this request: {user_message}")
        ]

        try:
            response = await self.llm.ainvoke(messages)
            content = response.content

            # Try to parse JSON response
            import json
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # Fallback: extract JSON from markdown code block
                import re
                match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if match:
                    result = json.loads(match.group(1))
                else:
                    raise ValueError("Could not parse JSON response")

            # Store in conversation history
            self.conversation_history.append({
                "user": user_message,
                "classification": result
            })

            return result

        except Exception as e:
            # Fallback classification
            return {
                "task_type": "unknown",
                "task_description": user_message,
                "confidence": 0.0,
                "context": {},
                "error": str(e)
            }

    async def generate_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an execution plan based on collected context.

        Args:
            context: Project context and task details

        Returns:
            Step-by-step plan for execution
        """
        plan_prompt = f"""Given the following task context, generate a detailed execution plan:

Task Type: {context.get('task_type')}
Description: {context.get('task_description')}

Available tools:
- file_read: Read file contents
- file_write: Create new files
- file_edit: Modify existing files
- url_fetch: Retrieve documentation
- github_cli: Git operations (status, commit, branch, PR)
- jira_cli: Ticket operations
- aider: LLM-assisted coding

Generate a plan as a JSON array of steps:
[
    {{
        "step_number": 1,
        "action": "tool_name",
        "parameters": {{}},
        "reasoning": "why this step is needed"
    }}
]
"""

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=plan_prompt)
        ]

        try:
            response = await self.llm.ainvoke(messages)
            content = response.content

            import json
            import re

            # Try to parse JSON
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # Extract from markdown
                match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if match:
                    result = json.loads(match.group(1))
                else:
                    # Try to find array directly
                    match = re.search(r'\[.*\]', content, re.DOTALL)
                    if match:
                        result = json.loads(match.group(0))
                    else:
                        raise ValueError("Could not parse plan")

            return {"plan": result}

        except Exception as e:
            return {
                "plan": [],
                "error": str(e)
            }

    def get_history(self) -> list:
        """Get conversation history."""
        return self.conversation_history
