# ULCA Configuration File
# Copy this file and modify the settings as needed

# LLM API Configuration
OLLAMA_API_BASE = "http://localhost:11434/api/generate"
MODEL_NAME = "claude-3.5-sonnet"

# API Request Settings
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30
MAX_TOKENS = 4000

# Model Parameters
TEMPERATURE = 0.1
TOP_P = 0.9

# File Operations
PROJECT_CONTEXT_FILE = "project_context.json"
MAX_FILE_SIZE_MB = 100  # Maximum file size to process

# Terminal Settings
COMMAND_TIMEOUT = 300  # 5 minutes
SAFE_COMMANDS = [
    "ls", "cat", "head", "tail", "grep", "find", "pwd", "whoami",
    "git", "npm", "yarn", "pip", "python", "node", "java", "javac",
    "gradle", "mvn", "xcodebuild", "flutter", "dart", "cargo"
]

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "ulca.log"

# UI Settings
ENABLE_COLORS = True
SHOW_TIMESTAMPS = True
MAX_CONVERSATION_HISTORY = 20

# Safety Settings
REQUIRE_CONFIRMATION_FOR = [
    "rm", "del", "delete", "overwrite", "modify", "change"
]

# Project Templates (optional)
PROJECT_TEMPLATES = {
    "python_flask": {
        "description": "Python Flask web application",
        "files": ["app.py", "requirements.txt", "README.md"]
    },
    "react_typescript": {
        "description": "React TypeScript application with Vite",
        "files": ["package.json", "src/App.tsx", "README.md"]
    },
    "android_kotlin": {
        "description": "Android Kotlin application",
        "files": ["app/build.gradle", "app/src/main/AndroidManifest.xml"]
    }
}
