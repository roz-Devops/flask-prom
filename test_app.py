# test_app.py

import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test client
        self.client = app.test_client()
        self.client.testing = True

    @patch('app.execute_mysql_query')
    def test_query_primary(self, mock_execute_query):
        # Mock the database response for primary colors
        mock_execute_query.return_value = [{'id': 1, 'name': 'Red', 'color_type': 'primary'}]

        response = self.client.get('/query?type=primary')
        data = response.get_json()

        # Check the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [{'id': 1, 'name': 'Red', 'color_type': 'primary'}])
    
    @patch('app.execute_mysql_query')
    def test_query_basic(self, mock_execute_query):
        # Mock the database response for basic colors
        mock_execute_query.return_value = [{'id': 2, 'name': 'Blue', 'color_type': 'basic'}]

        response = self.client.get('/query?type=basic')
        data = response.get_json()

        # Check the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [{'id': 2, 'name': 'Blue', 'color_type': 'basic'}])

    @patch('app.execute_mysql_query')
    def test_query_all(self, mock_execute_query):
        # Mock the database response for all colors
        mock_execute_query.return_value = [
            {'id': 1, 'name': 'Red', 'color_type': 'primary'},
            {'id': 2, 'name': 'Blue', 'color_type': 'basic'}
        ]

        response = self.client.get('/query')
        data = response.get_json()

        # Check the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [
            {'id': 1, 'name': 'Red', 'color_type': 'primary'},
            {'id': 2, 'name': 'Blue', 'color_type': 'basic'}
        ])

    def test_welcome(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to hell", response.data)

if __name__ == '__main__':
    unittest.main()
