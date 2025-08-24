#!/usr/bin/env python3
"""
ULCA Desktop GUI Application
A modern desktop interface for the Universal Local Claude Agent
"""

import sys
import os
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTextEdit, QLineEdit, QPushButton, QLabel, QTreeWidget,
    QTreeWidgetItem, QTabWidget, QTextBrowser, QProgressBar, QStatusBar,
    QToolBar, QMenuBar, QFileDialog, QMessageBox, QDialog, QDialogButtonBox,
    QVBoxLayout as QVBox, QHBoxLayout as QHBox, QFormLayout, QSpinBox,
    QComboBox, QCheckBox, QGroupBox, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QSettings, QSize, QMimeData,
    QUrl, QPropertyAnimation, QEasingCurve, QRect
)
from PyQt6.QtGui import (
    QFont, QFontMetrics, QTextCursor, QTextCharFormat, QColor,
    QPalette, QIcon, QAction, QKeySequence, QPixmap, QDragEnterEvent,
    QDropEvent, QTextOption
)

# Import the existing ULCA backend
from universal_claude_agent import ULCAgent

class LLMWorker(QThread):
    """Worker thread for LLM API calls"""
    response_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)
    
    def __init__(self, agent: ULCAgent, prompt: str):
        super().__init__()
        self.agent = agent
        self.prompt = prompt
        
    def run(self):
        try:
            # Emit progress updates
            self.progress_updated.emit(25)
            
            # Call the LLM
            response = self.agent.process_user_input(self.prompt)
            
            self.progress_updated.emit(100)
            self.response_received.emit(response)
            
        except Exception as e:
            self.error_occurred.emit(str(e))

class ConfirmationDialog(QDialog):
    """Modal dialog for file operation confirmations"""
    def __init__(self, parent=None, operation: str = "", details: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Confirm Operation")
        self.setModal(True)
        self.setMinimumSize(500, 300)
        
        layout = QVBox()
        
        # Operation description
        operation_label = QLabel(f"Operation: {operation}")
        operation_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        layout.addWidget(operation_label)
        
        # Details
        if details:
            details_text = QTextEdit()
            details_text.setPlainText(details)
            details_text.setReadOnly(True)
            details_text.setMaximumHeight(150)
            layout.addWidget(QLabel("Details:"))
            layout.addWidget(details_text)
        
        # Warning
        warning_label = QLabel("⚠️ This operation will modify your project files.")
        warning_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        layout.addWidget(warning_label)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

class CodeEditor(QTextEdit):
    """Enhanced text editor with syntax highlighting"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        
    def setup_editor(self):
        # Set monospace font
        font = QFont("Consolas", 10)
        font.setFixedPitch(True)
        self.setFont(font)
        
        # Set tab width
        self.setTabStopDistance(QFontMetrics(font).horizontalAdvance(' ') * 4)
        
        # Enable line wrapping
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#2b2b2b"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#a9b7c6"))
        self.setPalette(palette)
        
    def set_content(self, content: str, file_path: str = ""):
        """Set editor content and apply syntax highlighting"""
        self.setPlainText(content)
        self.apply_syntax_highlighting(file_path)
        
    def apply_syntax_highlighting(self, file_path: str):
        """Apply basic syntax highlighting based on file extension"""
        if not file_path:
            return
            
        extension = Path(file_path).suffix.lower()
        
        # Define colors for different syntax elements
        colors = {
            'keywords': QColor("#cc7832"),
            'strings': QColor("#6a8759"),
            'comments': QColor("#808080"),
            'numbers': QColor("#6897bb"),
            'functions': QColor("#ffc66d")
        }
        
        # Apply highlighting based on file type
        if extension in ['.py', '.pyw']:
            self.highlight_python(colors)
        elif extension in ['.js', '.jsx', '.ts', '.tsx']:
            self.highlight_javascript(colors)
        elif extension in ['.kt', '.java']:
            self.highlight_java_kotlin(colors)
        elif extension in ['.swift']:
            self.highlight_swift(colors)
            
    def highlight_python(self, colors):
        """Apply Python syntax highlighting"""
        keywords = ['def', 'class', 'import', 'from', 'as', 'if', 'else', 'elif', 
                   'for', 'while', 'try', 'except', 'finally', 'with', 'return', 
                   'True', 'False', 'None', 'self', 'lambda', 'yield', 'async', 'await']
        
        self.highlight_keywords(keywords, colors['keywords'])
        
    def highlight_javascript(self, colors):
        """Apply JavaScript/TypeScript syntax highlighting"""
        keywords = ['function', 'const', 'let', 'var', 'if', 'else', 'for', 'while',
                   'try', 'catch', 'finally', 'return', 'class', 'extends', 'import',
                   'export', 'default', 'async', 'await', 'new', 'this', 'super']
        
        self.highlight_keywords(keywords, colors['keywords'])
        
    def highlight_java_kotlin(self, colors):
        """Apply Java/Kotlin syntax highlighting"""
        keywords = ['public', 'private', 'protected', 'class', 'interface', 'enum',
                   'if', 'else', 'for', 'while', 'try', 'catch', 'finally', 'return',
                   'new', 'this', 'super', 'static', 'final', 'abstract', 'extends',
                   'implements', 'import', 'package', 'fun', 'val', 'var', 'when']
        
        self.highlight_keywords(keywords, colors['keywords'])
        
    def highlight_swift(self, colors):
        """Apply Swift syntax highlighting"""
        keywords = ['func', 'class', 'struct', 'enum', 'protocol', 'extension',
                   'if', 'else', 'for', 'while', 'guard', 'defer', 'return',
                   'var', 'let', 'init', 'self', 'super', 'import', 'public',
                   'private', 'internal', 'final', 'override', 'convenience']
        
        self.highlight_keywords(keywords, colors['keywords'])
        
    def highlight_keywords(self, keywords, color):
        """Highlight keywords in the text"""
        cursor = self.textCursor()
        format = QTextCharFormat()
        format.setForeground(color)
        format.setFontWeight(QFont.Weight.Bold)
        
        for keyword in keywords:
            cursor = self.document().find(keyword, cursor)
            if not cursor.isNull():
                cursor.mergeCharFormat(format)

class FileExplorer(QTreeWidget):
    """File explorer tree widget"""
    file_selected = pyqtSignal(str)  # Emits file path when file is selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_explorer()
        self.project_dir = None
        
    def setup_explorer(self):
        self.setHeaderLabel("Project Files")
        self.setColumnCount(1)
        self.itemClicked.connect(self.on_item_clicked)
        
    def set_project_directory(self, project_dir: str):
        """Set the project directory and populate the tree"""
        self.project_dir = Path(project_dir)
        self.clear()
        
        # Add project root
        root_item = QTreeWidgetItem(self)
        root_item.setText(0, self.project_dir.name)
        root_item.setIcon(0, self.style().standardIcon(self.style().StandardPixmap.SP_DirIcon))
        root_item.setData(0, Qt.ItemDataRole.UserRole, str(self.project_dir))
        
        self.populate_tree(root_item, self.project_dir)
        self.expandItem(root_item)
        
    def populate_tree(self, parent_item: QTreeWidgetItem, directory: Path):
        """Recursively populate the tree with directory contents"""
        try:
            for item in sorted(directory.iterdir()):
                if item.name.startswith('.'):  # Skip hidden files
                    continue
                    
                tree_item = QTreeWidgetItem(parent_item)
                tree_item.setText(0, item.name)
                
                if item.is_dir():
                    tree_item.setIcon(0, self.style().standardIcon(self.style().StandardPixmap.SP_DirIcon))
                    tree_item.setData(0, Qt.ItemDataRole.UserRole, str(item))
                    self.populate_tree(tree_item, item)
                else:
                    # Set appropriate icon based on file type
                    icon = self.get_file_icon(item)
                    tree_item.setIcon(0, icon)
                    tree_item.setData(0, Qt.ItemDataRole.UserRole, str(item))
                    
        except PermissionError:
            # Skip directories we can't access
            pass
            
    def get_file_icon(self, file_path: Path) -> QIcon:
        """Get appropriate icon for file type"""
        extension = file_path.suffix.lower()
        
        if extension in ['.py']:
            return self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogDetailedView)
        elif extension in ['.js', '.ts', '.jsx', '.tsx']:
            return self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogDetailedView)
        elif extension in ['.html', '.css']:
            return self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogDetailedView)
        elif extension in ['.json', '.xml', '.yaml', '.yml']:
            return self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogDetailedView)
        else:
            return self.style().standardIcon(self.style().StandardPixmap.SP_FileIcon)
            
    def on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle item click events"""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and Path(file_path).is_file():
            self.file_selected.emit(file_path)

class ChatWidget(QWidget):
    """Chat interface widget"""
    # Signal emitted when user sends a message
    message_sent = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBox()
        
        # Chat history display
        self.chat_display = QTextBrowser()
        self.chat_display.setOpenExternalLinks(True)
        self.chat_display.setStyleSheet("""
            QTextBrowser {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBox()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        self.setLayout(layout)
        
    def add_message(self, sender: str, message: str, message_type: str = "user"):
        """Add a message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        if message_type == "user":
            html = f'<div style="margin: 10px 0;"><b style="color: #007bff;">{sender}</b> <span style="color: #6c757d;">({timestamp})</span><br>{message}</div>'
        elif message_type == "assistant":
            html = f'<div style="margin: 10px 0;"><b style="color: #28a745;">{sender}</b> <span style="color: #6c757d;">({timestamp})</span><br>{message}</div>'
        elif message_type == "system":
            html = f'<div style="margin: 10px 0;"><b style="color: #6c757d;">{sender}</b> <span style="color: #6c757d;">({timestamp})</span><br>{message}</div>'
        else:
            html = f'<div style="margin: 10px 0;">{message}</div>'
            
        self.chat_display.append(html)
        
        # Scroll to bottom
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def send_message(self):
        """Send the current message"""
        message = self.input_field.text().strip()
        if message:
            self.add_message("You", message, "user")
            self.input_field.clear()
            # Emit signal for the main window to handle
            self.message_sent.emit(message)

class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.agent = None
        self.current_file = None
        self.settings = QSettings("ULCA", "DesktopGUI")
        
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_statusbar()
        
        # Initialize agent
        self.init_agent()
        
    def add_chat_message(self, sender: str, message: str, message_type: str = "user"):
        """Add a message to the chat widget"""
        if hasattr(self, 'chat_widget'):
            self.chat_widget.add_message(sender, message, message_type)
        
    def setup_ui(self):
        """Setup the main user interface"""
        self.setWindowTitle("ULCA - Universal Local Claude Agent")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBox()
        
        # Left panel: File explorer
        self.file_explorer = FileExplorer()
        self.file_explorer.file_selected.connect(self.open_file)
        self.file_explorer.setMaximumWidth(300)
        main_layout.addWidget(self.file_explorer)
        
        # Center panel: Main content area
        center_panel = QWidget()
        center_layout = QVBox()
        
        # Tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Chat tab
        self.chat_widget = ChatWidget()
        # Connect the chat widget's message signal to the main window handler
        self.chat_widget.message_sent.connect(self.handle_user_message)
        self.tab_widget.addTab(self.chat_widget, "Chat")
        
        # Code editor tab
        self.code_editor = CodeEditor()
        self.tab_widget.addTab(self.code_editor, "Code Editor")
        
        # Terminal output tab
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        self.tab_widget.addTab(self.terminal_output, "Terminal")
        
        center_layout.addWidget(self.tab_widget)
        center_panel.setLayout(center_layout)
        main_layout.addWidget(center_panel)
        
        # Right panel: Project info and TODO
        right_panel = QWidget()
        right_layout = QVBox()
        right_panel.setMaximumWidth(300)
        
        # Project info
        project_group = QGroupBox("Project Info")
        project_layout = QVBox()
        
        self.project_dir_label = QLabel("Project: Not set")
        self.project_dir_label.setWordWrap(True)
        project_layout.addWidget(self.project_dir_label)
        
        self.status_label = QLabel("Status: Initializing...")
        project_layout.addWidget(self.status_label)
        
        project_group.setLayout(project_layout)
        right_layout.addWidget(project_group)
        
        # TODO list
        todo_group = QGroupBox("TODO List")
        todo_layout = QVBox()
        
        self.todo_display = QTextBrowser()
        self.todo_display.setMaximumHeight(200)
        todo_layout.addWidget(self.todo_display)
        
        todo_group.setLayout(todo_layout)
        right_layout.addWidget(todo_group)
        
        # LLM status
        llm_group = QGroupBox("LLM Status")
        llm_layout = QVBox()
        
        self.llm_status_label = QLabel("Status: Disconnected")
        llm_layout.addWidget(self.llm_status_label)
        
        self.llm_progress = QProgressBar()
        self.llm_progress.setVisible(False)
        llm_layout.addWidget(self.llm_progress)
        
        llm_group.setLayout(llm_layout)
        right_layout.addWidget(llm_group)
        
        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)
        
        central_widget.setLayout(main_layout)
        
    def setup_menu(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_project_action = QAction("&Open Project...", self)
        open_project_action.setShortcut(QKeySequence.StandardKey.Open)
        open_project_action.triggered.connect(self.open_project)
        file_menu.addAction(open_project_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        settings_action = QAction("&Settings...", self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        test_llm_action = QAction("&Test LLM Connection", self)
        test_llm_action.triggered.connect(self.test_llm_connection)
        tools_menu.addAction(test_llm_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_toolbar(self):
        """Setup the toolbar"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Open project button
        open_project_action = QAction("📁 Open Project", self)
        open_project_action.triggered.connect(self.open_project)
        toolbar.addAction(open_project_action)
        
        # Save file button
        save_file_action = QAction("💾 Save", self)
        save_file_action.triggered.connect(self.save_current_file)
        toolbar.addAction(save_file_action)
        
        toolbar.addSeparator()
        
        # Test LLM button
        test_llm_action = QAction("🧪 Test LLM", self)
        test_llm_action.triggered.connect(self.test_llm_connection)
        toolbar.addAction(test_llm_action)
        
    def setup_statusbar(self):
        """Setup the status bar"""
        self.statusBar().showMessage("Ready")
        
    def init_agent(self):
        """Initialize the ULCA agent"""
        try:
            # Get current working directory
            project_dir = os.getcwd()
            
            # Create agent
            self.agent = ULCAgent(project_dir)
            
            # Update UI
            self.project_dir_label.setText(f"Project: {Path(project_dir).name}")
            self.status_label.setText(f"Status: {self.agent.context.get('current_status', 'Ready')}")
            
            # Populate file explorer
            self.file_explorer.set_project_directory(project_dir)
            
            # Update TODO list
            self.update_todo_display()
            
                    # Add welcome message
            self.add_chat_message("ULCA", "Hello! I'm your Universal Local Claude Agent. I'm ready to help you with your project development. What would you like to work on?", "system")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize agent: {str(e)}")
            
    def apply_settings(self):
        """Apply settings changes to the UI"""
        # Apply editor settings
        font_family = self.settings.value("editor/font_family", "Consolas")
        font_size = self.settings.value("editor/font_size", 10, type=int)
        
        font = QFont(font_family, font_size)
        font.setFixedPitch(True)
        self.code_editor.setFont(font)
        
        # Apply tab width
        tab_width = self.settings.value("editor/tab_width", 4, type=int)
        self.code_editor.setTabStopDistance(QFontMetrics(font).horizontalAdvance(' ') * tab_width)
        
        # Apply UI visibility settings
        toolbar_visible = self.settings.value("ui/show_toolbar", True, type=bool)
        if hasattr(self, 'toolBar'):
            self.toolBar().setVisible(toolbar_visible)
        
        statusbar_visible = self.settings.value("ui/show_statusbar", True, type=bool)
        self.statusBar().setVisible(statusbar_visible)
        
        # Update LLM configuration if agent exists
        if self.agent:
            api_base = self.settings.value("llm/api_base_url", "http://localhost:11434/api/generate")
            model_name = self.settings.value("llm/model_name", "claude-3.5-sonnet")
            
            # Update agent configuration
            if hasattr(self.agent, 'context') and 'llm_config' in self.agent.context:
                self.agent.context['llm_config']['api_base'] = api_base
                self.agent.context['llm_config']['model'] = model_name
                self.agent._save_context()
            
    def open_project(self):
        """Open a project directory"""
        project_dir = QFileDialog.getExistingDirectory(
            self, "Select Project Directory", os.getcwd()
        )
        
        if project_dir:
            try:
                # Change to project directory
                os.chdir(project_dir)
                
                # Reinitialize agent
                self.init_agent()
                
                self.statusBar().showMessage(f"Opened project: {project_dir}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open project: {str(e)}")
                
    def open_file(self, file_path: str):
        """Open a file in the code editor"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.code_editor.set_content(content, file_path)
            self.current_file = file_path
            
            # Switch to code editor tab
            self.tab_widget.setCurrentIndex(1)
            
            # Update status
            self.statusBar().showMessage(f"Opened: {Path(file_path).name}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")
            
    def save_current_file(self):
        """Save the current file"""
        if not self.current_file:
            QMessageBox.warning(self, "Warning", "No file is currently open")
            return
            
        try:
            content = self.code_editor.toPlainText()
            
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            self.statusBar().showMessage(f"Saved: {Path(self.current_file).name}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
            
    def handle_user_message(self, message: str):
        """Handle user message from chat widget"""
        if not self.agent:
            self.add_chat_message("System", "Agent not initialized", "system")
            return
            
        # Show LLM progress
        self.llm_progress.setVisible(True)
        self.llm_progress.setValue(0)
        self.llm_status_label.setText("Status: Processing...")
        
        # Create worker thread for LLM call
        self.llm_worker = LLMWorker(self.agent, message)
        self.llm_worker.response_received.connect(self.handle_llm_response)
        self.llm_worker.error_occurred.connect(self.handle_llm_error)
        self.llm_worker.progress_updated.connect(self.llm_progress.setValue)
        
        # Start worker
        self.llm_worker.start()
        
    def handle_llm_response(self, response: str):
        """Handle LLM response"""
        # Hide progress
        self.llm_progress.setVisible(False)
        self.llm_status_label.setText("Status: Ready")
        
        # Add response to chat
        self.add_chat_message("Claude", response, "assistant")
        
        # Check if response needs confirmation
        if "AWAITING_CONFIRMATION" in response:
            self.show_confirmation_dialog()
            
        # Update TODO list if needed
        self.update_todo_display()
        
        # Update status
        self.status_label.setText(f"Status: {self.agent.context.get('current_status', 'Ready')}")
        
    def handle_llm_error(self, error: str):
        """Handle LLM error"""
        self.llm_progress.setVisible(False)
        self.llm_status_label.setText("Status: Error")
        
        self.add_chat_message("System", f"Error: {error}", "system")
        
    def show_confirmation_dialog(self):
        """Show confirmation dialog for file operations"""
        if not self.agent or not self.agent.confirmation_mode:
            return
            
        dialog = ConfirmationDialog(
            self,
            operation="File Operation",
            details=self.agent.pending_question or "The agent wants to perform a file operation."
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # User confirmed
            self.handle_confirmation_response("yes")
        else:
            # User denied
            self.handle_confirmation_response("no")
            
    def handle_confirmation_response(self, response: str):
        """Handle user confirmation response"""
        if not self.agent:
            return
            
        # Send confirmation to agent
        if hasattr(self.agent, '_handle_confirmation_response'):
            result = self.agent._handle_confirmation_response(response)
            self.add_chat_message("Claude", result, "assistant")
            
    def update_todo_display(self):
        """Update the TODO list display"""
        if not self.agent:
            return
            
        todos = self.agent.context.get('todo_list', [])
        if todos:
            todo_text = "\n".join([f"• {todo}" for todo in todos])
        else:
            todo_text = "No TODO items"
            
        self.todo_display.setPlainText(todo_text)
        
    def test_llm_connection(self):
        """Test LLM connection"""
        if not self.agent:
            QMessageBox.warning(self, "Warning", "Agent not initialized")
            return
            
        try:
            self.llm_status_label.setText("Status: Testing...")
            
            # Simple test prompt
            test_prompt = "Please respond with 'Connection test successful!' and nothing else."
            
            # Create worker for test
            self.test_worker = LLMWorker(self.agent, test_prompt)
            self.test_worker.response_received.connect(self.handle_test_response)
            self.test_worker.error_occurred.connect(self.handle_test_error)
            
            self.test_worker.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to test LLM: {str(e)}")
            
    def handle_test_response(self, response: str):
        """Handle test response"""
        if "Connection test successful" in response:
            self.llm_status_label.setText("Status: Connected")
            QMessageBox.information(self, "Success", "LLM connection test successful!")
        else:
            self.llm_status_label.setText("Status: Error")
            QMessageBox.warning(self, "Warning", f"Unexpected test response: {response}")
            
    def handle_test_error(self, error: str):
        """Handle test error"""
        self.llm_status_label.setText("Status: Error")
        QMessageBox.critical(self, "Error", f"LLM test failed: {error}")
        
    def show_settings(self):
        """Show settings dialog"""
        from settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Apply settings changes
            self.apply_settings()
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About ULCA", 
                         "ULCA - Universal Local Claude Agent\n\n"
                         "A desktop GUI for the Universal Local Claude Agent\n"
                         "Version 1.0.0\n\n"
                         "Built with PyQt6")
                         
    def closeEvent(self, event):
        """Handle application close event"""
        # Save settings
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
        event.accept()

def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("ULCA Desktop")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("ULCA")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Restore window state
    settings = QSettings("ULCA", "DesktopGUI")
    geometry = settings.value("geometry")
    if geometry:
        window.restoreGeometry(geometry)
        
    window_state = settings.value("windowState")
    if window_state:
        window.restoreState(window_state)
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
