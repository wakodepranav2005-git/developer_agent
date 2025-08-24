#!/usr/bin/env python3
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
