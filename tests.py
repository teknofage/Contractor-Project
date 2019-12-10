from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

from bson.objectid import ObjectId
from app import app
from unittest import TestCase, main
from unittest.mock import patch

class AppTests(TestCase): 
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 
    
    @patch('pymongo.collection.Collection.find')
    def test_show_coaches(self, mock_find):
        """Test the All Coaches page."""
        # Set up our fake data.
        fake_coaches = [
            {'name': 'Rui Costa'},
            {'name': 'Sir Alf Ramsey'}
        ]
        # Set fake data as the mock return value for `find`.
        mock_find.return_value = fake_coaches

        # Load the URL being tested.
        result = self.app.get('/coaches')

        # Check that status code is OK.
        self.assertEqual(result.status_code, 200)

        # Check that the page content contains the 2 songs in our test data.
        page_content = result.get_data(as_text=True)
        self.assertIn('Rui Costa', page_content)
        self.assertIn('Sir Alf Ramsey', page_content)
        
        
    @patch('pymongo.collection.Collection.insert_one')
    def test_leagues_submit(self, mock_insert_one):
        """Test the League Creation route."""
        # Set up our fake data.
        fake_name = 'Invisible Field'
        fake_age_group = '5-8, 70-80'
        fake_level = 'Alternative'
        fake_website = 'www.fakefootballfield.com'
        

        # Wrap the data as key-value pairs in a dictionary, so that it will
        # match what the route expects to receive.
        post_data = {
            'name': fake_name,
            'age_group': fake_age_group,
            'level': fake_level,
            'website': fake_website
        }
        # Make a POST request to the URL being tested, and pass in our data.
        result = self.app.post('/leagues', data=post_data)

        # Check that the status code is 302 (meaning that we are redirected).
        self.assertEqual(result.status_code, 302)

        # Ensure that a song object would have been added to the database.
        mock_insert_one.assert_called_with(post_data)