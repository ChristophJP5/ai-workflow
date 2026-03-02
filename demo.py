#!/usr/bin/env python3
"""
Demo script for AI Workflow system.
Shows the system in action without requiring a full LLM setup.
"""

import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from ui.chat_interface import ChatInterface


async def demo():
    """Run a demo of the workflow system."""
    print("🦞 AI Workflow Demo")
    print("=" * 50)
    print()
    
    # Initialize chat interface
    chat = ChatInterface()
    await chat.initialize()
    
    if not chat.initialized:
        print("\n⚠ Demo mode: Using mock LLM")
    
    # Demo messages
    demos = [
        "Fix the login bug in auth.py",
        "Add a logout button to the navbar",
        "The API is returning 500 errors",
        "Create a new user profile page"
    ]
    
    for i, message in enumerate(demos, 1):
        print(f"\n{'='*50}")
        print(f"Demo {i}: {message}")
        print('='*50)
        
        if chat.initialized:
            result = await chat.process_single(message)
            print(f"\n✅ Result: {result.get('status', 'unknown')}")
            print(f"   Workflow: {result.get('workflow_type', 'unknown')}")
            print(f"   ID: {result.get('workflow_id', 'N/A')}")
        else:
            print("\n⚠ System not initialized")
        
        await asyncio.sleep(0.5)
    
    print("\n" + "="*50)
    print("✅ Demo complete!")
    print("="*50)


if __name__ == "__main__":
    asyncio.run(demo())
