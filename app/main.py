#!/usr/bin/env python3
"""
AI Workflow - LLM-Driven Development Workflows
Main entry point for the application.
"""

import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.chat_interface import ChatInterface


def main():
    """Main entry point."""
    print("🦞 AI Workflow - LLM-Driven Development System")
    print("=" * 50)
    print()

    # Start the chat interface
    chat = ChatInterface()
    asyncio.run(chat.run())


if __name__ == "__main__":
    main()
