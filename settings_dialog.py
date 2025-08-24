#!/usr/bin/env python3
"""
Settings Dialog for ULCA GUI
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QComboBox, QCheckBox, QDialogButtonBox, QGroupBox,
    QLabel, QTabWidget, QWidget, QTextEdit, QPushButton
)
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QFont

class SettingsDialog(QDialog):
    """Settings dialog for ULCA GUI"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("ULCA", "DesktopGUI")
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the settings dialog UI"""
        self.setWindowTitle("ULCA Settings")
        self.setMinimumSize(600, 500)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # General tab
        general_tab = self.create_general_tab()
        tab_widget.addTab(general_tab, "General")
        
        # LLM tab
        llm_tab = self.create_llm_tab()
        tab_widget.addTab(llm_tab, "LLM Configuration")
        
        # Editor tab
        editor_tab = self.create_editor_tab()
        tab_widget.addTab(editor_tab, "Editor")
        
        # Advanced tab
        advanced_tab = self.create_advanced_tab()
        tab_widget.addTab(advanced_tab, "Advanced")
        
        layout.addWidget(tab_widget)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
    def create_general_tab(self):
        """Create the general settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Project settings
        project_group = QGroupBox("Project Settings")
        project_layout = QFormLayout()
        
        self.default_project_dir = QLineEdit()
        self.default_project_dir.setPlaceholderText("Leave empty to use current directory")
        project_layout.addRow("Default Project Directory:", self.default_project_dir)
        
        self.auto_save = QCheckBox("Auto-save files")
        self.auto_save.setChecked(True)
        project_layout.addRow("", self.auto_save)
        
        self.auto_save_interval = QSpinBox()
        self.auto_save_interval.setRange(1, 60)
        self.auto_save_interval.setValue(5)
        self.auto_save_interval.setSuffix(" minutes")
        project_layout.addRow("Auto-save Interval:", self.auto_save_interval)
        
        project_group.setLayout(project_layout)
        layout.addWidget(project_group)
        
        # UI settings
        ui_group = QGroupBox("Interface Settings")
        ui_layout = QFormLayout()
        
        self.show_toolbar = QCheckBox("Show toolbar")
        self.show_toolbar.setChecked(True)
        ui_layout.addRow("", self.show_toolbar)
        
        self.show_statusbar = QCheckBox("Show status bar")
        self.show_statusbar.setChecked(True)
        ui_layout.addRow("", self.show_statusbar)
        
        self.remember_window_state = QCheckBox("Remember window size and position")
        self.remember_window_state.setChecked(True)
        ui_layout.addRow("", self.remember_window_state)
        
        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def create_llm_tab(self):
        """Create the LLM configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # API settings
        api_group = QGroupBox("API Configuration")
        api_layout = QFormLayout()
        
        self.api_base_url = QLineEdit()
        self.api_base_url.setPlaceholderText("http://localhost:11434/api/generate")
        api_layout.addRow("API Base URL:", self.api_base_url)
        
        self.model_name = QLineEdit()
        self.model_name.setPlaceholderText("claude-3.5-sonnet")
        api_layout.addRow("Model Name:", self.model_name)
        
        self.api_timeout = QSpinBox()
        self.api_timeout.setRange(10, 300)
        self.api_timeout.setValue(120)
        self.api_timeout.setSuffix(" seconds")
        api_layout.addRow("Request Timeout:", self.api_timeout)
        
        self.max_retries = QSpinBox()
        self.max_retries.setRange(1, 10)
        self.max_retries.setValue(3)
        api_layout.addRow("Max Retries:", self.max_retries)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Model parameters
        model_group = QGroupBox("Model Parameters")
        model_layout = QFormLayout()
        
        self.temperature = QSpinBox()
        self.temperature.setRange(0, 100)
        self.temperature.setValue(10)
        self.temperature.setSuffix(" (0.1)")
        model_layout.addRow("Temperature:", self.temperature)
        
        self.top_p = QSpinBox()
        self.top_p.setRange(1, 100)
        self.top_p.setValue(90)
        self.top_p.setSuffix(" (0.9)")
        model_layout.addRow("Top P:", self.top_p)
        
        self.max_tokens = QSpinBox()
        self.max_tokens.setRange(100, 10000)
        self.max_tokens.setValue(2000)
        self.max_tokens.setSuffix(" tokens")
        model_layout.addRow("Max Tokens:", self.max_tokens)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def create_editor_tab(self):
        """Create the editor settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Font settings
        font_group = QGroupBox("Font Settings")
        font_layout = QFormLayout()
        
        self.editor_font_family = QComboBox()
        self.editor_font_family.addItems(["Consolas", "Monaco", "Courier New", "DejaVu Sans Mono"])
        font_layout.addRow("Font Family:", self.editor_font_family)
        
        self.editor_font_size = QSpinBox()
        self.editor_font_size.setRange(8, 24)
        self.editor_font_size.setValue(10)
        font_layout.addRow("Font Size:", self.editor_font_size)
        
        self.tab_width = QSpinBox()
        self.tab_width.setRange(2, 8)
        self.tab_width.setValue(4)
        self.tab_width.setSuffix(" spaces")
        font_layout.addRow("Tab Width:", self.tab_width)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # Editor behavior
        behavior_group = QGroupBox("Editor Behavior")
        behavior_layout = QFormLayout()
        
        self.line_numbers = QCheckBox("Show line numbers")
        self.line_numbers.setChecked(True)
        behavior_layout.addRow("", self.line_numbers)
        
        self.syntax_highlighting = QCheckBox("Enable syntax highlighting")
        self.syntax_highlighting.setChecked(True)
        behavior_layout.addRow("", self.syntax_highlighting)
        
        self.auto_indent = QCheckBox("Auto-indent")
        self.auto_indent.setChecked(True)
        behavior_layout.addRow("", self.auto_indent)
        
        self.word_wrap = QCheckBox("Word wrap")
        behavior_layout.addRow("", self.word_wrap)
        
        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def create_advanced_tab(self):
        """Create the advanced settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Logging settings
        logging_group = QGroupBox("Logging")
        logging_layout = QFormLayout()
        
        self.log_level = QComboBox()
        self.log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level.setCurrentText("INFO")
        logging_layout.addRow("Log Level:", self.log_level)
        
        self.log_file = QLineEdit()
        self.log_file.setPlaceholderText("ulca_gui.log")
        logging_layout.addRow("Log File:", self.log_file)
        
        self.enable_debug = QCheckBox("Enable debug mode")
        logging_layout.addRow("", self.enable_debug)
        
        logging_group.setLayout(logging_layout)
        layout.addWidget(logging_group)
        
        # Performance settings
        performance_group = QGroupBox("Performance")
        performance_layout = QFormLayout()
        
        self.max_conversation_history = QSpinBox()
        self.max_conversation_history.setRange(10, 1000)
        self.max_conversation_history.setValue(100)
        performance_layout.addRow("Max Conversation History:", self.max_conversation_history)
        
        self.file_cache_size = QSpinBox()
        self.file_cache_size.setRange(10, 1000)
        self.file_cache_size.setValue(100)
        self.file_cache_size.setSuffix(" files")
        performance_layout.addRow("File Cache Size:", self.file_cache_size)
        
        performance_group.setLayout(performance_layout)
        layout.addWidget(performance_group)
        
        # Reset button
        reset_layout = QHBoxLayout()
        reset_layout.addStretch()
        
        reset_button = QPushButton("Reset to Defaults")
        reset_button.clicked.connect(self.reset_to_defaults)
        reset_layout.addWidget(reset_button)
        
        layout.addLayout(reset_layout)
        layout.addStretch()
        widget.setLayout(layout)
        return widget
        
    def load_settings(self):
        """Load current settings"""
        # General settings
        self.default_project_dir.setText(self.settings.value("general/default_project_dir", ""))
        self.auto_save.setChecked(self.settings.value("general/auto_save", True, type=bool))
        self.auto_save_interval.setValue(self.settings.value("general/auto_save_interval", 5, type=int))
        self.show_toolbar.setChecked(self.settings.value("ui/show_toolbar", True, type=bool))
        self.show_statusbar.setChecked(self.settings.value("ui/show_statusbar", True, type=bool))
        self.remember_window_state.setChecked(self.settings.value("ui/remember_window_state", True, type=bool))
        
        # LLM settings
        self.api_base_url.setText(self.settings.value("llm/api_base_url", "http://localhost:11434/api/generate"))
        self.model_name.setText(self.settings.value("llm/model_name", "claude-3.5-sonnet"))
        self.api_timeout.setValue(self.settings.value("llm/api_timeout", 120, type=int))
        self.max_retries.setValue(self.settings.value("llm/max_retries", 3, type=int))
        self.temperature.setValue(int(self.settings.value("llm/temperature", 0.1) * 100))
        self.top_p.setValue(int(self.settings.value("llm/top_p", 0.9) * 100))
        self.max_tokens.setValue(self.settings.value("llm/max_tokens", 2000, type=int))
        
        # Editor settings
        self.editor_font_family.setCurrentText(self.settings.value("editor/font_family", "Consolas"))
        self.editor_font_size.setValue(self.settings.value("editor/font_size", 10, type=int))
        self.tab_width.setValue(self.settings.value("editor/tab_width", 4, type=int))
        self.line_numbers.setChecked(self.settings.value("editor/line_numbers", True, type=bool))
        self.syntax_highlighting.setChecked(self.settings.value("editor/syntax_highlighting", True, type=bool))
        self.auto_indent.setChecked(self.settings.value("editor/auto_indent", True, type=bool))
        self.word_wrap.setChecked(self.settings.value("editor/word_wrap", False, type=bool))
        
        # Advanced settings
        self.log_level.setCurrentText(self.settings.value("advanced/log_level", "INFO"))
        self.log_file.setText(self.settings.value("advanced/log_file", "ulca_gui.log"))
        self.enable_debug.setChecked(self.settings.value("advanced/enable_debug", False, type=bool))
        self.max_conversation_history.setValue(self.settings.value("advanced/max_conversation_history", 100, type=int))
        self.file_cache_size.setValue(self.settings.value("advanced/file_cache_size", 100, type=int))
        
    def save_settings(self):
        """Save current settings"""
        # General settings
        self.settings.setValue("general/default_project_dir", self.default_project_dir.text())
        self.settings.setValue("general/auto_save", self.auto_save.isChecked())
        self.settings.setValue("general/auto_save_interval", self.auto_save_interval.value())
        self.settings.setValue("ui/show_toolbar", self.show_toolbar.isChecked())
        self.settings.setValue("ui/show_statusbar", self.show_statusbar.isChecked())
        self.settings.setValue("ui/remember_window_state", self.remember_window_state.isChecked())
        
        # LLM settings
        self.settings.setValue("llm/api_base_url", self.api_base_url.text())
        self.settings.setValue("llm/model_name", self.model_name.text())
        self.settings.setValue("llm/api_timeout", self.api_timeout.value())
        self.settings.setValue("llm/max_retries", self.max_retries.value())
        self.settings.setValue("llm/temperature", self.temperature.value() / 100.0)
        self.settings.setValue("llm/top_p", self.top_p.value() / 100.0)
        self.settings.setValue("llm/max_tokens", self.max_tokens.value())
        
        # Editor settings
        self.settings.setValue("editor/font_family", self.editor_font_family.currentText())
        self.settings.setValue("editor/font_size", self.editor_font_size.value())
        self.settings.setValue("editor/tab_width", self.tab_width.value())
        self.settings.setValue("editor/line_numbers", self.line_numbers.isChecked())
        self.settings.setValue("editor/syntax_highlighting", self.syntax_highlighting.isChecked())
        self.settings.setValue("editor/auto_indent", self.auto_indent.isChecked())
        self.settings.setValue("editor/word_wrap", self.word_wrap.isChecked())
        
        # Advanced settings
        self.settings.setValue("advanced/log_level", self.log_level.currentText())
        self.settings.setValue("advanced/log_file", self.log_file.text())
        self.settings.setValue("advanced/enable_debug", self.enable_debug.isChecked())
        self.settings.setValue("advanced/max_conversation_history", self.max_conversation_history.value())
        self.settings.setValue("advanced/file_cache_size", self.file_cache_size.value())
        
        self.settings.sync()
        
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        # Clear all settings
        self.settings.clear()
        
        # Reload with defaults
        self.load_settings()
        
    def accept(self):
        """Handle dialog acceptance"""
        self.save_settings()
        super().accept()
