#!/usr/bin/env python3
"""
Demo script for ULCA Desktop GUI
This script demonstrates the key features of the GUI application
"""

import os
import sys
import time
from pathlib import Path

def create_demo_project():
    """Create a demo project to showcase the GUI"""
    demo_dir = Path("ulca_demo_project")
    demo_dir.mkdir(exist_ok=True)
    
    # Create demo files
    files = {
        "main.py": '''#!/usr/bin/env python3
"""
Demo Flask Application
A simple web application to showcase ULCA capabilities
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to ULCA Demo App!",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/api/items', methods=['GET'])
def get_items():
    items = [
        {"id": 1, "name": "Item 1", "description": "First demo item"},
        {"id": 2, "name": "Item 2", "description": "Second demo item"},
        {"id": 3, "name": "Item 3", "description": "Third demo item"}
    ]
    return jsonify(items)

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    # In a real app, this would save to a database
    new_item = {
        "id": 4,  # This would be auto-generated
        "name": data['name'],
        "description": data.get('description', 'No description')
    }
    
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
''',
        
        "requirements.txt": '''flask==2.3.3
requests==2.31.0
python-dotenv==1.0.0
''',
        
        "README.md": '''# ULCA Demo Project

This is a demo project to showcase the ULCA Desktop GUI capabilities.

## Features

- **Flask Web API**: Simple REST API with CRUD operations
- **JSON Responses**: Clean API responses in JSON format
- **Error Handling**: Basic input validation and error responses
- **Modular Design**: Clean, well-structured Python code

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Open your browser to: http://localhost:5000

## API Endpoints

- `GET /` - Home page with app info
- `GET /api/items` - List all items
- `POST /api/items` - Create a new item

## Development

This project is designed to work with ULCA (Universal Local Claude Agent) for:
- Code generation and modification
- Bug fixes and improvements
- Feature additions
- Code review and optimization

## Next Steps

Try asking ULCA to:
- Add a database connection
- Implement user authentication
- Add more API endpoints
- Create unit tests
- Add logging and monitoring
''',
        
        "config.py": '''# Configuration file for ULCA Demo App

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database settings (for future use)
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///demo.db'
    
    # API settings
    API_TITLE = "ULCA Demo API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "A demo API to showcase ULCA capabilities"
    
    # Security settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
''',
        
        "tests/test_main.py": '''#!/usr/bin/env python3
"""
Unit tests for the main application
"""

import unittest
import json
from main import app

class TestMainApp(unittest.TestCase):
    """Test cases for the main Flask application"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        """Test the home endpoint"""
        response = self.app.get('/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertIn('status', data)
        self.assertIn('version', data)
        self.assertEqual(data['status'], 'running')
    
    def test_get_items_endpoint(self):
        """Test the get items endpoint"""
        response = self.app.get('/api/items')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Check first item structure
        first_item = data[0]
        self.assertIn('id', first_item)
        self.assertIn('name', first_item)
        self.assertIn('description', first_item)
    
    def test_create_item_endpoint(self):
        """Test the create item endpoint"""
        new_item = {
            "name": "Test Item",
            "description": "A test item for testing"
        }
        
        response = self.app.post('/api/items',
                               data=json.dumps(new_item),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)
        self.assertEqual(data['name'], new_item['name'])
        self.assertEqual(data['description'], new_item['description'])
    
    def test_create_item_validation(self):
        """Test item creation validation"""
        # Missing name
        invalid_item = {"description": "No name provided"}
        
        response = self.app.post('/api/items',
                               data=json.dumps(invalid_item),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
''',
        
        ".env.example": '''# Environment variables for ULCA Demo App
# Copy this file to .env and modify as needed

# Flask settings
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database settings
DATABASE_URL=sqlite:///demo.db

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
'''
    }
    
    # Create files
    for filename, content in files.items():
        file_path = demo_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created: {file_path}")
    
    # Create project context
    context = {
        "project_directory": str(demo_dir.absolute()),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "conversation_history": [
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "user_input": "Create a demo Flask application to showcase ULCA capabilities",
                "agent_response": "I'll create a comprehensive demo Flask application with API endpoints, configuration, and testing to showcase ULCA's development capabilities.",
                "action_taken": "created_demo_project"
            }
        ],
        "project_goal": "Create a demo Flask web application to showcase ULCA capabilities for development assistance",
        "todo_list": [
            "- Add database integration with SQLAlchemy",
            "- Implement user authentication system",
            "- Add API documentation with Swagger/OpenAPI",
            "- Create deployment configuration",
            "- Add monitoring and logging",
            "- Implement rate limiting and security features"
        ],
        "current_status": "demo_project_created",
        "file_operations": [
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "operation": "created",
                "file_path": "main.py",
                "description": "Main Flask application with API endpoints"
            },
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "operation": "created",
                "file_path": "requirements.txt",
                "description": "Python dependencies"
            },
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "operation": "created",
                "file_path": "README.md",
                "description": "Project documentation and setup instructions"
            },
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "operation": "created",
                "file_path": "config.py",
                "description": "Configuration management"
            },
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "operation": "created",
                "file_path": "tests/test_main.py",
                "description": "Unit tests for the application"
            },
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "operation": "created",
                "file_path": ".env.example",
                "description": "Environment variables template"
            }
        ],
        "build_attempts": [],
        "llm_config": {
            "model": "claude-3.5-sonnet",
            "api_base": "http://localhost:11434/api/generate"
        }
    }
    
    # Save context
    context_file = demo_dir / "project_context.json"
    import json
    with open(context_file, 'w', encoding='utf-8') as f:
        json.dump(context, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created project context: {context_file}")
    print(f"\n🎉 Demo project created successfully in: {demo_dir.absolute()}")
    
    return demo_dir

def main():
    """Main demo function"""
    print("🎭 ULCA Desktop GUI Demo")
    print("=" * 40)
    
    # Create demo project
    demo_dir = create_demo_project()
    
    print("\n📋 Demo Project Features:")
    print("• Flask web application with REST API")
    print("• Multiple file types (Python, Markdown, config files)")
    print("• Project structure with tests and documentation")
    print("• Pre-populated project context and TODO list")
    print("• Ready for ULCA development assistance")
    
    print(f"\n🚀 To test the GUI:")
    print(f"1. Change to the demo directory: cd {demo_dir}")
    print("2. Start the GUI: python ../ulca_gui.py")
    print("3. Or use the launcher: python ../run_gui.py")
    print("4. Explore the file explorer and chat with ULCA")
    
    print(f"\n💡 Try asking ULCA to:")
    print("• Add a new API endpoint")
    print("• Implement database integration")
    print("• Add error handling and validation")
    print("• Create additional test cases")
    
    print(f"\n📁 Demo project location: {demo_dir.absolute()}")
    print("🎯 The GUI will automatically load this project context!")

if __name__ == "__main__":
    main()
