#!/usr/bin/env python3
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
