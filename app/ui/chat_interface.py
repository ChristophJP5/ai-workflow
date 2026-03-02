#!/usr/bin/env python3
"""
Chat Interface - User interface for the workflow system.
"""

import asyncio
import os
from typing import Optional, Dict, Any
from pathlib import Path

# Add parent to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env file
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

from agent.agent import LLMAgent
from agent.router import WorkflowRouter


class ChatInterface:
    """
    Chat interface for user interaction.
    """

    WELCOME_MESSAGE = """
🦞 AI Workflow - LLM-Driven Development System
=============================================

I can help you with:
  • 🐛 Bugfix - Fix existing defects in your code
  • ✨ Feature - Implement new functionality

Just describe what you need, and I'll handle the rest!

Type 'quit' or 'exit' to leave.
"""

    def __init__(self):
        """Initialize the chat interface."""
        self.agent = None
        self.router = None
        self.initialized = False

    async def initialize(self) -> None:
        """Initialize the LLM agent and router."""
        print("🔄 Initializing AI Workflow system...")
        
        try:
            # Import LangChain and set up the agent
            from langchain_openai import ChatOpenAI
            from langchain_core.language_models import BaseLanguageModel
            
            # Check for NVIDIA API configuration
            nvidia_api_key = os.getenv("NVIDIA_API_KEY")
            nvidia_base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
            nvidia_model = os.getenv("NVIDIA_MODEL", "nvidia/mistralai/mistral-large-3-675b-instruct-2512")
            
            if nvidia_api_key:
                # Use NVIDIA API (OpenAI-compatible)
                llm = ChatOpenAI(
                    model=nvidia_model,
                    base_url=nvidia_base_url,
                    api_key=nvidia_api_key,
                    temperature=0.3,
                    max_tokens=4096
                )
                model_name = nvidia_model.split("/")[-1] if "/" in nvidia_model else nvidia_model
                print(f"   ✓ Connected to NVIDIA API ({model_name})")
            else:
                # Try Ollama as fallback
                try:
                    from langchain_community.llms import Ollama
                    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1")
                    ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
                    llm = Ollama(model=ollama_model, base_url=ollama_base)
                    print(f"   ✓ Connected to Ollama ({ollama_model})")
                except Exception:
                    # Fallback to Mock LLM
                    llm = MockLLM()
                    print("   ⚠ Using mock LLM")
                    print("   Set NVIDIA_API_KEY in .env or start Ollama to use a real LLM")
            
            self.agent = LLMAgent(llm)
            self.router = WorkflowRouter()
            self.initialized = True
            print("   ✓ System ready\n")
            
        except Exception as e:
            print(f"   ✗ Initialization error: {e}")
            print("   ⚠ Running in demo mode\n")
            self.initialized = False

    async def run(self) -> None:
        """Run the chat interface."""
        print(self.WELCOME_MESSAGE)
        
        # Initialize components
        await self.initialize()
        
        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = await self._get_input()
                
                if not user_input:
                    continue
                    
                user_input = user_input.strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                    
                # Process the message
                await self._process_message(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

    async def _get_input(self) -> str:
        """Get user input."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, "\n👤 You: ")

    async def _process_message(self, message: str) -> None:
        """
        Process a user message.

        Args:
            message: User message
        """
        if not self.initialized:
            print("\n⚠ System not initialized. Please wait...")
            return
            
        print("\n🤖 Processing...")
        
        try:
            # Step 1: Classify the request
            print("   📊 Classifying request...")
            classification = await self.agent.classify_request(message)
            print(f"   → Task type: {classification.get('task_type', 'unknown')}")
            print(f"   → Confidence: {classification.get('confidence', 0):.0%}")
            
            # Step 2: Route to workflow
            print("\n   🔀 Routing to workflow...")
            result = await self.router.route(classification)
            
            # Step 3: Display result
            print("\n" + "=" * 50)
            print("📋 RESULT")
            print("=" * 50)
            print(f"Workflow ID: {result.get('workflow_id', 'N/A')}")
            print(f"Status: {result.get('status', 'unknown')}")
            print(f"Type: {result.get('workflow_type', 'unknown')}")
            
            if result.get('validation', {}).get('success'):
                print("\n✅ Validation: PASSED")
            else:
                print("\n⚠ Validation: PENDING")
                
            print("\n💡 Next steps:")
            print("   - Review the changes")
            print("   - Run tests if applicable")
            print("   - Commit and push when ready")
            
        except Exception as e:
            print(f"\n❌ Error processing message: {e}")

    async def process_single(self, message: str) -> Dict[str, Any]:
        """
        Process a single message and return result.
        Useful for API-style usage.

        Args:
            message: User message

        Returns:
            Result dictionary
        """
        if not self.initialized:
            await self.initialize()
            
        classification = await self.agent.classify_request(message)
        result = await self.router.route(classification)
        return result


class MockLLM:
    """Mock LLM for demo purposes."""
    
    async def ainvoke(self, messages):
        """Mock invoke."""
        from langchain_core.messages import AIMessage
        
        # Simple classification based on keywords
        content = str(messages[-1].content) if messages else ""
        
        if any(word in content.lower() for word in ['bug', 'fix', 'error', 'issue', 'broken']):
            response = '{"task_type": "bugfix", "task_description": "' + content + '", "confidence": 0.8}'
        else:
            response = '{"task_type": "feature", "task_description": "' + content + '", "confidence": 0.7}'
        
        return AIMessage(content=response)


def main():
    """Main entry point."""
    chat = ChatInterface()
    asyncio.run(chat.run())


if __name__ == "__main__":
    main()
