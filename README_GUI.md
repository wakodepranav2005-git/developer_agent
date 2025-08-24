# ULCA Desktop GUI

A modern desktop GUI application for the Universal Local Claude Agent (ULCA), transforming it from a CLI tool into an IDE-like development assistant.

## Features

### 🖥️ Main Interface
- **Three-panel layout**: File explorer, main content area, and project info sidebar
- **Tabbed content**: Chat interface, code editor, and terminal output
- **Modern design**: Clean, intuitive interface with proper spacing and typography

### 💬 Chat Interface
- **Multi-turn conversations**: Seamless chat with the LLM agent
- **Message history**: Scrollable conversation view with timestamps
- **Message types**: Different styling for user, assistant, and system messages

### 📁 File Explorer
- **Tree view**: Hierarchical project file structure
- **File icons**: Visual indicators for different file types
- **Click to open**: Single-click file opening in the code editor

### ✏️ Code Editor
- **Syntax highlighting**: Support for Python, JavaScript, TypeScript, Java, Kotlin, and Swift
- **Monospace font**: Optimized for code readability
- **Configurable**: Font size, family, tab width, and other settings
- **File operations**: Open, edit, and save files with confirmation

### 🔧 Modal Confirmations
- **Safety first**: All file operations require explicit user approval
- **Clear descriptions**: Detailed information about proposed changes
- **Blocking dialogs**: Prevents further commands until user acts

### ⚙️ Settings & Configuration
- **Comprehensive settings**: General, LLM, editor, and advanced options
- **Persistent storage**: Settings saved between sessions
- **LLM configuration**: API endpoints, model parameters, timeouts
- **Editor customization**: Fonts, syntax highlighting, behavior options

### 🚀 LLM Integration
- **Background processing**: Non-blocking LLM calls using worker threads
- **Progress indicators**: Visual feedback during API calls
- **Error handling**: Graceful handling of connection and API failures
- **Connection testing**: Built-in LLM connectivity testing

## Installation

### Prerequisites
- Python 3.8 or higher
- Local Claude model running via Ollama or similar
- PyQt6 for the GUI framework

### Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements_gui.txt
   ```

2. **Ensure your local LLM is running**:
   ```bash
   # If using Ollama
   ollama serve
   
   # Pull the Claude model
   ollama pull claude-3.5-sonnet
   ```

3. **Verify the backend works**:
   ```bash
   python universal_claude_agent.py
   ```

## Usage

### Starting the GUI

```bash
python ulca_gui.py
```

### Basic Workflow

1. **Open a project**: Use File → Open Project or the toolbar button
2. **Chat with the agent**: Type your development requests in the chat tab
3. **Review files**: Browse project structure in the left panel
4. **Edit code**: Click files to open them in the code editor
5. **Confirm changes**: Approve or deny file modifications via modal dialogs

### Key Features

#### File Operations
- **Opening files**: Click any file in the explorer to open it
- **Editing**: Modify code directly in the embedded editor
- **Saving**: Use Ctrl+S or the save button in the toolbar
- **Safety**: All modifications require explicit confirmation

#### LLM Interaction
- **Natural language**: Describe what you want to build or modify
- **Context awareness**: The agent maintains project context across sessions
- **Confirmation workflow**: Agent asks for permission before making changes
- **Progress tracking**: Visual indicators during LLM processing

#### Project Management
- **Context persistence**: Project state saved in `project_context.json`
- **TODO tracking**: Automatic extraction and display of task lists
- **Status monitoring**: Real-time project and LLM status updates

## Configuration

### Settings Dialog

Access via **Tools → Settings** to configure:

- **General**: Project directories, auto-save, UI preferences
- **LLM**: API endpoints, model parameters, timeouts
- **Editor**: Fonts, syntax highlighting, behavior
- **Advanced**: Logging, performance, debugging

### LLM Configuration

The GUI integrates with your existing ULCA backend:

- **API Base URL**: Defaults to `http://localhost:11434/api/generate`
- **Model Name**: Defaults to `claude-3.5-sonnet`
- **Parameters**: Temperature, top-p, max tokens, timeouts
- **Retry Logic**: Automatic retry with exponential backoff

## Architecture

### Modular Design

```
ulca_gui.py          # Main application and window
settings_dialog.py    # Settings configuration dialog
universal_claude_agent.py  # Backend agent (existing)
```

### Key Components

- **MainWindow**: Central application window with layout management
- **ChatWidget**: Chat interface with message handling
- **CodeEditor**: Syntax-highlighted text editor
- **FileExplorer**: Tree-based file browser
- **LLMWorker**: Background thread for API calls
- **ConfirmationDialog**: Modal dialogs for user approval

### Threading Model

- **Main thread**: UI updates and user interactions
- **Worker threads**: LLM API calls and file operations
- **Signal-based communication**: Qt signals for thread-safe updates

## Troubleshooting

### Common Issues

1. **LLM Connection Failed**:
   - Verify Ollama is running: `ollama serve`
   - Check API endpoint in settings
   - Test connection via Tools → Test LLM Connection

2. **GUI Not Starting**:
   - Ensure PyQt6 is installed: `pip install PyQt6`
   - Check Python version: `python --version`
   - Verify all dependencies: `pip install -r requirements_gui.txt`

3. **File Operations Failing**:
   - Check file permissions
   - Verify project directory is writable
   - Look for error messages in the status bar

4. **Settings Not Persisting**:
   - Check application data directory permissions
   - Verify QSettings is working on your platform
   - Try resetting to defaults in settings dialog

### Debug Mode

Enable debug mode in **Tools → Settings → Advanced** to get more detailed logging.

## Development

### Extending the GUI

The modular architecture makes it easy to add new features:

1. **New widgets**: Create custom widget classes
2. **Additional tabs**: Extend the tab widget in MainWindow
3. **Settings**: Add new configuration options to SettingsDialog
4. **LLM integration**: Extend LLMWorker for new API features

### Code Style

- Follow PEP 8 for Python code
- Use Qt naming conventions for GUI elements
- Maintain separation between UI and business logic
- Document all public methods and classes

## License

This GUI application is part of the ULCA project and follows the same licensing terms.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the existing ULCA documentation
3. Open an issue on the project repository
4. Check the logs for detailed error information

---

**Note**: This GUI application is designed to work seamlessly with your existing ULCA backend. It maintains all the safety features and confirmation workflows while providing a modern, intuitive interface for development work.
