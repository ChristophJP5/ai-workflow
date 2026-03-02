# Quick Start Guide

Get up and running with AI Workflow in 5 minutes!

## Prerequisites

- Python 3.10+
- pip (Python package manager)
- Optional: Ollama or other LLM backend

## Installation

### Step 1: Clone/Navigate to the project

```bash
cd /home/polaris/.openclaw/workspace/ai-workflow
```

### Step 2: Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment (optional)

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Running the System

### Option 1: Interactive Chat

```bash
python app/main.py
```

Then start chatting:
```
👤 You: Fix the bug in the login function
```

### Option 2: Demo Mode

```bash
python demo.py
```

This shows automated examples of the system in action.

### Option 3: Programmatic Usage

```python
import asyncio
from app.ui.chat_interface import ChatInterface

async def main():
    chat = ChatInterface()
    await chat.initialize()
    
    result = await chat.process_single("Add a new feature")
    print(result)

asyncio.run(main())
```

## Testing Workflows

### Test Bugfix Workflow

```
👤 You: The login function is broken, it returns None for valid users
```

### Test Feature Workflow

```
👤 You: Add a dark mode toggle to the settings page
```

## Troubleshooting

### "Module not found" errors

Make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### Ollama connection errors

If using Ollama, make sure it's running:
```bash
ollama serve
```

Or switch to mock LLM (no setup required).

### Import errors

Make sure you're in the right directory:
```bash
cd /home/polaris/.openclaw/workspace/ai-workflow
python app/main.py
```

## Next Steps

1. **Read the README.md** - Full documentation
2. **Configure your LLM** - Set up Ollama or another backend
3. **Connect to GitHub/Jira** - Optional integrations
4. **Customize workflows** - Modify for your needs

## Getting Help

- Check `README.md` for detailed documentation
- Review `app/workflows/` for workflow implementations
- Look at `app/tools/` for tool implementations

---

Happy coding! 🦞
