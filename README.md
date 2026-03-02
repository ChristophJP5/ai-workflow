# AI Workflow - LLM-Driven Development System

A minimal Python + LangChain system that allows users to chat with an LLM which can trigger structured development workflows.

## 🎯 Goal

Create a conversational interface for development tasks with two primary workflows:
- **🐛 Bugfix** - Diagnose and fix existing defects
- **✨ Feature** - Implement new functionality

## 📋 Features

- Natural language task intake
- LLM-powered task classification
- Structured workflow execution
- Tool integration (File I/O, GitHub, Jira, Aider)
- Comprehensive logging
- Chat-based UI

## 🏗️ Architecture

```
User
  │
  ▼
Chat UI
  │
  ▼
LangChain LLM Agent
  │
  ├── Workflow Router
  │     │
  │     ├── Bugfix Workflow
  │     │   ├─ File Tools
  │     │   ├─ Aider (LLM coding)
  │     │   ├─ GitHub CLI
  │     │   ├─ Jira CLI
  │     │   └─ URL Fetch
  │     │
  │     └── Feature Workflow
  │         ├─ File Tools
  │         ├─ Aider (LLM coding)
  │         ├─ GitHub CLI
  │         ├─ Jira CLI
  │         └─ URL Fetch
  │
  ▼
Logging System
  │
  ▼
Result → Chat UI
```

## 📁 Project Structure

```
ai-workflow/
├── app/
│   ├── main.py                 # Entry point
│   ├── agent/
│   │   ├── agent.py            # LLM Agent
│   │   └── router.py           # Workflow Router
│   ├── workflows/
│   │   ├── base_workflow.py    # Base workflow class
│   │   ├── bugfix_workflow.py  # Bugfix workflow
│   │   └── feature_workflow.py # Feature workflow
│   ├── tools/
│   │   ├── file_tools.py       # File operations
│   │   ├── github_cli.py       # GitHub integration
│   │   ├── jira_cli.py         # Jira integration
│   │   ├── url_fetch.py        # URL fetching
│   │   └── aider_tool.py       # Aider integration
│   ├── logging/
│   │   └── workflow_logger.py  # Logging system
│   └── ui/
│       └── chat_interface.py   # Chat UI
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ai-workflow
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app/main.py
```

### 3. Start Chatting

```
🦞 AI Workflow - LLM-Driven Development System
=============================================

I can help you with:
  • 🐛 Bugfix - Fix existing defects in your code
  • ✨ Feature - Implement new functionality

Just describe what you need, and I'll handle the rest!

Type 'quit' or 'exit' to leave.

👤 You: Fix the login bug in auth.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# GitHub (optional)
GITHUB_TOKEN=your_token_here

# Jira (optional)
JIRA_SERVER=https://your-company.atlassian.net
JIRA_TOKEN=your_token_here
```

## 📊 Workflow Steps

### Bugfix Workflow

1. **User Request** - Natural language description
2. **Workflow Selection** - LLM classifies as bugfix
3. **Context Collection** - Gather files, git state, issue data
4. **Planning** - Generate debugging plan
5. **Code Interaction** - Execute fixes
6. **External Operations** - Update Jira, commit to GitHub
7. **Validation** - Verify the fix
8. **Result Packaging** - Summary and next steps
9. **Logging** - All actions logged
10. **UI Response** - Return results to user

### Feature Workflow

1. **User Request** - Natural language description
2. **Workflow Selection** - LLM classifies as feature
3. **Context Collection** - Gather requirements, existing code
4. **Planning** - Generate implementation plan
5. **Code Interaction** - Implement feature
6. **External Operations** - Create PR, update Jira
7. **Validation** - Test the feature
8. **Result Packaging** - Summary and next steps
9. **Logging** - All actions logged
10. **UI Response** - Return results to user

## 🛠️ Tools

| Tool | Purpose |
|------|---------|
| File Read | Read project files |
| File Write | Create new files |
| File Edit | Modify existing files |
| URL Fetch | Retrieve documentation |
| GitHub CLI | Commit, branch, PR |
| Jira CLI | Read/update tickets |
| Aider | LLM-assisted coding |

## 📝 Logging

All workflow executions are logged to `logs/workflow-YYYY-MM-DD.jsonl` with:
- Timestamp
- Workflow ID
- Step name
- Result status
- Tool executions
- LLM decisions

## 🧪 Example Usage

### Bugfix Example

```
👤 You: The login function in auth.py is failing with None user

🤖 Processing...
   📊 Classifying request...
   → Task type: bugfix
   → Confidence: 85%

   🔀 Routing to workflow...

🐛 Starting Bugfix Workflow (ID: a1b2c3d4)
==================================================

📋 Step 1: Collecting context...
   Found 3 relevant files

📝 Step 2: Generating debugging plan...
   Generated 3 steps

🔧 Step 3: Executing fix...
   Executing: analyze
   Executing: fix
   Executing: test

✅ Step 4: Validating results...

📦 Step 5: Packaging results...

✅ Bugfix Workflow completed (ID: a1b2c3d4)

==================================================
📋 RESULT
==================================================
Workflow ID: a1b2c3d4
Status: completed
Type: bugfix

✅ Validation: PASSED

💡 Next steps:
   - Review the changes
   - Run tests if applicable
   - Commit and push when ready
```

### Feature Example

```
👤 You: Add a logout button to the navbar

🤖 Processing...
   📊 Classifying request...
   → Task type: feature
   → Confidence: 92%

✨ Starting Feature Workflow (ID: e5f6g7h8)
...
```

## 🔄 Expected MVP Behavior

1. ✅ User describes a task in chat
2. ✅ LLM classifies the request
3. ✅ Router selects the workflow
4. ✅ Workflow gathers project context
5. ✅ LLM generates plan
6. ✅ Tools execute code changes
7. ✅ Validation runs
8. ✅ Results returned to UI

## 🎯 Capabilities

- [x] Conversational task intake
- [x] Structured development workflows
- [x] Automated code interaction
- [x] External system integration
- [x] Observable execution via logs
- [ ] Real-time progress updates
- [ ] Interactive approval steps
- [ ] Multi-file context management

## 📚 License

MIT

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a PR

---

Built with ❤️ using LangChain and Python
