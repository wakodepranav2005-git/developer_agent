#!/usr/bin/env python3
"""
Universal Local Claude Agent (ULCA)
A stateful, interactive development partner that works with local Claude models
to assist with any project type while maintaining persistent context.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import requests
import shutil

# Configuration
OLLAMA_API_BASE = "http://localhost:11434/api/generate"
PROJECT_CONTEXT_FILE = "project_context.json"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 120  # Increased timeout for GGUF models

class ULCAgent:
    """Universal Local Claude Agent - Main agent class"""
    
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir).resolve()
        self.context_file = self.project_dir / PROJECT_CONTEXT_FILE
        self.context = self._load_or_create_context()
        self.confirmation_mode = False
        self.pending_action = None
        self.pending_question = None
        
    def _load_or_create_context(self) -> Dict[str, Any]:
        """Load existing context or create new one"""
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    context = json.load(f)
                print(f"📁 Loaded existing project context from {PROJECT_CONTEXT_FILE}")
                return context
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  Error loading context: {e}. Creating new context.")
        
        # Create new context
        context = {
            "project_directory": str(self.project_dir),
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "conversation_history": [],
            "project_goal": "",
            "todo_list": [],
            "current_status": "awaiting_user_input",
            "file_operations": [],
            "build_attempts": [],
            "llm_config": {
                "model": "claude-3.5-sonnet",
                "api_base": OLLAMA_API_BASE
            }
        }
        self._save_context(context)
        print(f"🆕 Created new project context in {self.project_dir}")
        return context
    
    def _save_context(self, context: Optional[Dict[str, Any]] = None):
        """Save context to file"""
        if context is None:
            context = self.context
        context["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(context, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"❌ Error saving context: {e}")
    
    def _get_file_listing(self) -> str:
        """Get current directory listing"""
        try:
            result = subprocess.run(
                ["ls", "-la"], 
                cwd=self.project_dir, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error listing files: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Timeout getting file listing"
        except Exception as e:
            return f"Error getting file listing: {e}"
    
    def _execute_command(self, command: str, capture_output: bool = True) -> Tuple[int, str, str]:
        """Execute a shell command safely"""
        print(f"🔄 Executing: {command}")
        
        try:
            if capture_output:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    cwd=self.project_dir, 
                    capture_output=True, 
                    text=True, 
                    timeout=300
                )
                return result.returncode, result.stdout, result.stderr
            else:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    cwd=self.project_dir, 
                    timeout=300
                )
                return result.returncode, "", ""
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out after 5 minutes"
        except Exception as e:
            return -1, "", f"Error executing command: {e}"
    
    def _call_llm(self, prompt: str) -> str:
        """Call local LLM API with retry logic"""
        payload = {
            "model": "claude-3.5-sonnet",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 2000,  # Use num_predict for Llama models
                "stop": ["\n\nHuman:", "\n\nUser:", "Human:", "User:"]  # Stop tokens
            }
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                print(f"🔄 Attempting LLM call (attempt {attempt + 1}/{MAX_RETRIES})...")
                response = requests.post(
                    OLLAMA_API_BASE, 
                    json=payload, 
                    timeout=REQUEST_TIMEOUT
                )
                response.raise_for_status()
                
                result = response.json()
                if "response" in result:
                    return result["response"].strip()
                else:
                    print(f"⚠️  Unexpected response format: {result}")
                    return "Error: Unexpected response format from LLM"
                    
            except requests.exceptions.Timeout:
                if attempt < MAX_RETRIES - 1:
                    print(f"⏰ Timeout on attempt {attempt + 1}/{MAX_RETRIES}. Retrying...")
                    time.sleep(5)  # Wait 5 seconds before retry
                else:
                    return f"Error: LLM request timed out after {MAX_RETRIES} attempts. The model might be busy or too slow."
            except requests.exceptions.ConnectionError:
                if attempt < MAX_RETRIES - 1:
                    print(f"🔌 Connection error on attempt {attempt + 1}/{MAX_RETRIES}. Retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return f"Error: Failed to connect to LLM after {MAX_RETRIES} attempts. Check if Ollama is running."
            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"⚠️  API call failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return f"Error: Failed to communicate with LLM after {MAX_RETRIES} attempts: {e}"
            except Exception as e:
                return f"Error: Unexpected error calling LLM: {e}"
        
        return "Error: Failed to get response from LLM"
    
    def _build_system_prompt(self, user_input: str) -> str:
        """Build comprehensive system prompt for LLM"""
        file_listing = self._get_file_listing()
        
        system_prompt = f"""You are ULCA (Universal Local Claude Agent), a helpful, cautious, and intelligent coding assistant. You work with users to develop any type of project (Android, iOS, web, desktop, etc.).

CRITICAL SAFETY RULES:
1. NEVER delete or overwrite existing files without explicit user confirmation
2. Always ask for permission before making destructive changes
3. Be extremely cautious with file operations
4. If unsure about anything, ask the user for clarification

CURRENT PROJECT CONTEXT:
- Project Directory: {self.project_dir}
- Project Goal: {self.context.get('project_goal', 'Not defined')}
- Current Status: {self.context.get('current_status', 'Unknown')}
- TODO List: {json.dumps(self.context.get('todo_list', []), indent=2)}

CONVERSATION HISTORY:
{self._format_conversation_history()}

CURRENT DIRECTORY CONTENTS:
{file_listing}

USER'S LATEST REQUEST:
{user_input}

YOUR RESPONSE MUST INCLUDE:
1. Your analysis and thought process
2. A specific, actionable next step
3. If you need to modify files, clearly state what you'll do and ask for permission
4. If the task is complex, break it down into a TODO list
5. If you need clarification, ask specific questions

FORMAT YOUR RESPONSE CLEARLY AND STRUCTURED. Always end with a clear question or request for permission if you plan to take action."""

        return system_prompt
    
    def _format_conversation_history(self) -> str:
        """Format conversation history for LLM prompt"""
        history = self.context.get('conversation_history', [])
        if not history:
            return "No previous conversation."
        
        formatted = []
        for i, entry in enumerate(history[-10:], 1):  # Last 10 entries
            timestamp = entry.get('timestamp', 'Unknown')
            user_input = entry.get('user_input', '')
            agent_response = entry.get('agent_response', '')
            formatted.append(f"--- Entry {i} ({timestamp}) ---")
            formatted.append(f"User: {user_input}")
            formatted.append(f"Agent: {agent_response}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    def _update_context(self, user_input: str, agent_response: str, action_taken: str = ""):
        """Update context with new interaction"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "agent_response": agent_response,
            "action_taken": action_taken
        }
        
        self.context["conversation_history"].append(entry)
        self.context["current_status"] = "awaiting_user_input"
        self._save_context()
    
    def _handle_file_operation(self, operation: str) -> bool:
        """Handle file operations with user confirmation"""
        print(f"\n🔧 Proposed file operation: {operation}")
        response = input("Do you approve this operation? [Y/n]: ").strip().lower()
        
        if response in ['', 'y', 'yes']:
            return True
        return False
    
    def _create_file(self, file_path: str, content: str) -> bool:
        """Create a new file with content"""
        full_path = self.project_dir / file_path
        
        if full_path.exists():
            if not self._handle_file_operation(f"Overwrite existing file: {file_path}"):
                return False
        
        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created file: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error creating file {file_path}: {e}")
            return False
    
    def _modify_file(self, file_path: str, content: str) -> bool:
        """Modify an existing file"""
        full_path = self.project_dir / file_path
        
        if not full_path.exists():
            print(f"⚠️  File {file_path} doesn't exist. Creating it instead.")
            return self._create_file(file_path, content)
        
        if not self._handle_file_operation(f"Modify existing file: {file_path}"):
            return False
        
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Modified file: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error modifying file {file_path}: {e}")
            return False
    
    def _delete_file(self, file_path: str) -> bool:
        """Delete a file with confirmation"""
        full_path = self.project_dir / file_path
        
        if not full_path.exists():
            print(f"⚠️  File {file_path} doesn't exist.")
            return False
        
        if not self._handle_file_operation(f"DELETE file: {file_path}"):
            return False
        
        try:
            full_path.unlink()
            print(f"✅ Deleted file: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error deleting file {file_path}: {e}")
            return False
    
    def _parse_llm_response(self, response: str) -> Tuple[str, List[str], List[str], bool, str]:
        """Parse LLM response for actions, TODO items, and confirmation requests"""
        actions = []
        todo_items = []
        needs_confirmation = False
        confirmation_question = ""
        
        # Look for TODO items (lines starting with - or * or numbered)
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('-', '*', '•')) or (line and line[0].isdigit() and '. ' in line):
                if 'todo' in line.lower() or 'task' in line.lower():
                    todo_items.append(line)
        
        # Detect confirmation requests
        response_lower = response.lower()
        confirmation_indicators = [
            'should i proceed', 'shall i proceed', 'do you want me to',
            'would you like me to', 'can i proceed', 'may i proceed',
            'do you approve', 'should i continue', 'shall i continue',
            'do you want me to continue', 'would you like me to continue'
        ]
        
        for indicator in confirmation_indicators:
            if indicator in response_lower:
                needs_confirmation = True
                # Extract the question around the confirmation request
                start_idx = response_lower.find(indicator)
                if start_idx != -1:
                    # Get context around the confirmation request
                    context_start = max(0, start_idx - 100)
                    context_end = min(len(response), start_idx + 200)
                    confirmation_question = response[context_start:context_end].strip()
                    break
        
        return response, actions, todo_items, needs_confirmation, confirmation_question
    
    def _update_todo_list(self, new_items: List[str]):
        """Update TODO list with new items"""
        current_todos = set(self.context.get('todo_list', []))
        for item in new_items:
            if item.strip():
                current_todos.add(item.strip())
        
        self.context['todo_list'] = list(current_todos)
        self._save_context()
    
    def _update_project_goal(self, goal: str):
        """Update project goal"""
        self.context['project_goal'] = goal
        self._save_context()
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and return agent response"""
        print(f"\n🤔 Processing: {user_input}")
        
        # Build comprehensive prompt
        system_prompt = self._build_system_prompt(user_input)
        
        # Call LLM
        print("🧠 Consulting Claude...")
        llm_response = self._call_llm(system_prompt)
        
        if llm_response.startswith("Error:"):
            print(f"❌ {llm_response}")
            return "I'm sorry, but I encountered an error communicating with my local Claude model. Please check that the model is running and accessible."
        
        # Parse response
        parsed_response, actions, todo_items, needs_confirmation, confirmation_question = self._parse_llm_response(llm_response)
        
        # Update TODO list if new items found
        if todo_items:
            self._update_todo_list(todo_items)
            print(f"📝 Updated TODO list with {len(todo_items)} new items")
        
        # Check if LLM is asking for confirmation
        if needs_confirmation:
            self.confirmation_mode = True
            self.pending_action = "llm_confirmation"
            self.pending_question = confirmation_question
            print(f"\n🔒 CONFIRMATION REQUIRED:")
            print(f"🤖 Claude is asking for your approval:")
            print(f"   {confirmation_question}")
            print(f"\n💬 Please respond with 'yes' or 'no' to continue.")
            print(f"💡 You can also type 'exit' to cancel or 'clear' to reset.")
            return "AWAITING_CONFIRMATION"
        
        # Update context
        self._update_context(user_input, parsed_response)
        
        return parsed_response
    
    def run_interactive_loop(self):
        """Main interactive loop"""
        print("\n" + "="*60)
        print("🚀 Universal Local Claude Agent (ULCA) - Ready!")
        print("="*60)
        print(f"📁 Working in: {self.project_dir}")
        print(f"💾 Context file: {self.context_file}")
        print(f"🎯 Project goal: {self.context.get('project_goal', 'Not defined')}")
        print(f"📋 TODO items: {len(self.context.get('todo_list', []))}")
        print("\n💡 I'm ready to help! What would you like to work on?")
        print("   (Type 'exit' to quit, 'help' for commands, 'status' for current state)")
        print("-" * 60)
        
        while True:
            try:
                # Show confirmation mode indicator
                if self.confirmation_mode:
                    prompt = "\n🔒 CONFIRMATION REQUIRED (yes/no): "
                else:
                    prompt = "\n🎯 You: "
                
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye! Your project context has been saved.")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if user_input.lower() == 'status':
                    self._show_status()
                    continue
                
                if user_input.lower() == 'todo':
                    self._show_todo()
                    continue
                
                if user_input.lower() == 'files':
                    self._show_files()
                    continue
                
                if user_input.lower() == 'test':
                    self._test_llm_connection()
                    continue
                
                if user_input.lower() == 'ls':
                    self._show_files()
                    continue
                
                if user_input.lower() == 'confirm':
                    if self.confirmation_mode:
                        print(f"🔒 Currently awaiting confirmation for: {self.pending_question}")
                    else:
                        print("✅ No confirmation pending - agent is ready for new commands")
                    continue
                
                if user_input.lower() == 'clear':
                    if self.confirmation_mode:
                        print("🧹 Clearing confirmation mode")
                        self.confirmation_mode = False
                        self.pending_action = None
                        self.pending_question = None
                    else:
                        print("✅ No confirmation mode to clear")
                    continue
                
                # Check if we're in confirmation mode
                if self.confirmation_mode:
                    response = self._handle_confirmation_response(user_input)
                    print(f"\n🤖 Claude: {response}")
                    continue
                
                # Process user input
                response = self.process_user_input(user_input)
                
                if response == "AWAITING_CONFIRMATION":
                    # Don't print response, we're waiting for confirmation
                    continue
                
                print(f"\n🤖 Claude: {response}")
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted by user. Type 'exit' to quit properly.")
            except EOFError:
                print("\n\n👋 End of input. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("Please try again or type 'exit' to quit.")
    
    def _show_help(self):
        """Show help information"""
        help_text = """
📚 ULCA Commands:
- help: Show this help message
- status: Show current project status
- todo: Show current TODO list
- files: Show current directory contents
- test: Test LLM connection
- confirm: Show confirmation status
- clear: Clear confirmation mode
- exit/quit/q: Exit the program

💡 Usage Tips:
- Be specific about what you want to build
- I'll ask for permission before making changes
- I maintain context across sessions
- I can work with any project type
        """
        print(help_text)
    
    def _show_status(self):
        """Show current project status"""
        confirmation_status = "🔒 AWAITING CONFIRMATION" if self.confirmation_mode else "✅ Ready"
        status_text = f"""
📊 Project Status:
- Directory: {self.project_dir}
- Goal: {self.context.get('project_goal', 'Not defined')}
- Status: {self.context.get('current_status', 'Unknown')}
- TODO Items: {len(self.context.get('todo_list', []))}
- Conversations: {len(self.context.get('conversation_history', []))}
- Last Updated: {self.context.get('last_updated', 'Unknown')}
- Agent State: {confirmation_status}
        """
        print(status_text)
    
    def _show_todo(self):
        """Show current TODO list"""
        todos = self.context.get('todo_list', [])
        if not todos:
            print("📋 No TODO items defined yet.")
        else:
            print("📋 Current TODO List:")
            for i, todo in enumerate(todos, 1):
                print(f"  {i}. {todo}")
    
    def _show_files(self):
        """Show current directory contents"""
        print("📁 Current Directory Contents:")
        print(self._get_file_listing())
    
    def _test_llm_connection(self):
        """Test LLM connection with a simple prompt"""
        print("🧪 Testing LLM connection...")
        test_prompt = "Please respond with 'Connection test successful!' and nothing else."
        
        try:
            response = self._call_llm(test_prompt)
            if response.startswith("Error:"):
                print(f"❌ {response}")
            else:
                print(f"✅ LLM connection successful!")
                print(f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    def _handle_confirmation_response(self, user_input: str) -> str:
        """Handle user confirmation responses"""
        if not self.confirmation_mode:
            return "No confirmation pending"
        
        user_input_lower = user_input.lower().strip()
        
        if user_input_lower in ['yes', 'y', 'proceed', 'continue', 'approve']:
            # User approved the action
            print(f"✅ Confirmation received: PROCEEDING with action")
            self.confirmation_mode = False
            self.pending_action = None
            self.pending_question = None
            
            # Send the confirmation back to LLM to continue
            follow_up_prompt = f"User has confirmed: '{user_input}'. Please proceed with the action you were planning."
            try:
                return self._call_llm(follow_up_prompt)
            except Exception as e:
                return f"Error continuing with action: {e}. Please provide a new instruction."
            
        elif user_input_lower in ['no', 'n', 'cancel', 'stop', 'deny']:
            # User denied the action
            print(f"❌ Confirmation received: CANCELLING action")
            self.confirmation_mode = False
            self.pending_action = None
            self.pending_question = None
            
            return "Action cancelled by user. What would you like to do instead?"
            
        elif user_input_lower in ['exit', 'quit', 'q']:
            # User wants to exit confirmation mode
            print(f"🚪 Exiting confirmation mode")
            self.confirmation_mode = False
            self.pending_action = None
            self.pending_question = None
            
            return "Confirmation mode exited. What would you like to do?"
            
        else:
            # Unclear response, ask for clarification
            return f"I didn't understand your response '{user_input}'. Please respond with 'yes', 'no', or 'exit' to continue."


def main():
    """Main entry point"""
    # Get project directory
    project_dir = os.getcwd()
    
    # Check if we're in a valid directory
    if not os.path.exists(project_dir):
        print(f"❌ Error: Directory {project_dir} does not exist.")
        sys.exit(1)
    
    # Check if we can write to the directory
    if not os.access(project_dir, os.W_OK):
        print(f"❌ Error: No write permission for directory {project_dir}")
        sys.exit(1)
    
    try:
        # Create and run agent
        agent = ULCAgent(project_dir)
        agent.run_interactive_loop()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your setup and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
