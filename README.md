# Universal Local Claude Agent (ULCA)

🚀 **Transform your local Claude 3.5 Sonnet GGUF model into a flexible, stateful, and interactive development partner!**

ULCA is a Python-based agent that works with your local Claude model to assist with any project type (Android, iOS, web, desktop, etc.) while maintaining persistent context and ensuring safe file operations.

## ✨ Key Features

- **🔄 Persistent Context Management**: Maintains conversation history, project goals, and TODO lists across sessions
- **🛡️ Safe File Operations**: Never deletes or overwrites files without explicit user confirmation
- **🌐 Project-Agnostic**: Works with any project type and technology stack
- **💻 Terminal Integration**: Executes shell commands and captures output for analysis
- **🧠 Intelligent Chunking**: Breaks down complex tasks into manageable TODO lists
- **🔄 Self-Correction**: Analyzes build errors and proposes solutions
- **📱 Interactive Dialogue**: Continuous conversation loop for collaborative development

## 🚀 Quick Start

### Prerequisites

1. **Python 3.10+** installed on your system
2. **Local Claude model** running via Ollama or similar local API server
3. **Write permissions** in your project directory

### Installation

1. **Clone or download** the ULCA files to your project directory
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Ensure your local Claude model is running** (e.g., Ollama on `http://localhost:11434`)

### Usage

1. **Navigate to your project directory**:
   ```bash
   cd /path/to/your/project
   ```

2. **Run ULCA**:
   ```bash
   python universal_claude_agent.py
   ```

3. **Start collaborating!** Example conversation:
   ```
   🎯 You: This is an empty directory. I want to start a Python Flask API for a book library.
   
   🤖 Claude: I'll help you create a Flask API for a book library! Let me analyze what we need...
   
   I'll create the following structure:
   - Flask application with proper project layout
   - Basic API endpoints for CRUD operations
   - SQLite database setup
   - Requirements.txt with dependencies
   
   Should I proceed with creating this structure? [Y/n]
   ```

## 🔧 Configuration

### API Endpoint

The default configuration assumes Ollama running on `http://localhost:11434`. You can modify this in the script:

```python
OLLAMA_API_BASE = "http://localhost:11434/api/generate"
```

### Model Name

Update the model name if you're using a different Claude model:

```python
"model": "claude-3.5-sonnet"  # Change to your model name
```

## 📁 Project Context

ULCA creates and maintains a `project_context.json` file in your project directory that contains:

- **Conversation History**: Complete chat history with timestamps
- **Project Goal**: Overall objective for the project
- **TODO List**: Dynamic list of tasks to complete
- **Current Status**: Current agent state
- **File Operations**: Log of file changes
- **Build Attempts**: History of build commands and results

## 🎯 Built-in Commands

- **`help`** - Show available commands and usage tips
- **`status`** - Display current project status and context
- **`todo`** - Show current TODO list
- **`files`** - Display current directory contents
- **`exit`/`quit`/`q`** - Exit the program

## 🔒 Safety Features

- **File Protection**: Never deletes or overwrites files without explicit confirmation
- **Command Validation**: All shell commands are executed with proper error handling
- **Context Preservation**: All changes are logged and can be reviewed
- **User Approval**: Destructive operations require user confirmation

## 💡 Usage Examples

### Starting a New Project

```
🎯 You: I want to create a React TypeScript app with Vite for a task management system.

🤖 Claude: Great idea! Let me break this down into manageable steps...
```

### Modifying Existing Code

```
🎯 You: Add error handling to the login function in auth.js

🤖 Claude: I can see the auth.js file. I'll add comprehensive error handling...
```

### Debugging Build Issues

```
🎯 You: The build is failing with a TypeScript error

🤖 Claude: Let me analyze the error and propose a solution...
```

## 🏗️ Architecture

ULCA is built with a modular architecture:

- **ULCAgent Class**: Main agent logic and state management
- **Context Management**: Persistent JSON-based context storage
- **LLM Communication**: HTTP-based communication with local Claude API
- **File Operations**: Safe file creation, modification, and deletion
- **Terminal Integration**: Subprocess-based command execution
- **Interactive Loop**: Continuous conversation management

## 🔧 Troubleshooting

### Common Issues

1. **"Failed to communicate with LLM"**
   - Ensure your local Claude model is running
   - Check the API endpoint configuration
   - Verify network connectivity

2. **"No write permission"**
   - Check directory permissions
   - Ensure you're in the correct project directory

3. **"Model not found"**
   - Verify the model name in your Ollama setup
   - Update the model name in the script if needed

### Debug Mode

For troubleshooting, you can add debug logging by modifying the script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Advanced Features

### Custom File Operations

ULCA can handle any file type and operation:
- Create new files with proper directory structure
- Modify existing files with user confirmation
- Delete files with explicit approval
- Handle binary and text files appropriately

### Build Loop Management

When builds fail, ULCA:
1. Analyzes error logs
2. Proposes specific solutions
3. Gets user approval
4. Applies fixes
5. Retries the build
6. Continues until success or user intervention

### Intelligent Task Chunking

For complex projects, ULCA:
- Breaks down large goals into manageable tasks
- Maintains a dynamic TODO list
- Tracks progress across sessions
- Suggests next steps based on context

## 🤝 Contributing

ULCA is designed to be easily extensible. Key areas for customization:

- **LLM Integration**: Support for different local model APIs
- **File Operations**: Custom file type handlers
- **Build Systems**: Integration with specific build tools
- **UI Enhancements**: Alternative interfaces (GUI, web, etc.)

## 📄 License

This project is open source. Feel free to modify and adapt it for your needs.

## 🙏 Acknowledgments

- Built for local Claude 3.5 Sonnet GGUF models
- Designed for collaborative development workflows
- Inspired by the need for persistent, safe AI coding assistance

---

**Ready to transform your development workflow? Start ULCA in your project directory and begin collaborating with your local Claude model!** 🚀
