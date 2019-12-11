from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

from bson.objectid import ObjectId
from app import app
from unittest import TestCase, main as unittest_main, mock
from unittest.mock import patch

sample_id_list = ['hY7m5jjJ9mM','CQ85sUNBK7w']
# All of these are new mock data that we'll use
sample_coach_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_coach = {
    'name': 'Papa Smurf',
    'resume': 'Perennial winning coach of Smurf Cup',
    'qualifications': 'Can motivate ants',
    'reviews': 5
}
sample_form_data = {
    'name': sample_coach['name'],
    'resume': sample_coach['resume'],
    'qualifications': sample_coach['qualifications']
}


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
        
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_coach(self, mock_find):
        """Test showing a coach field."""
        mock_find.return_value = sample_coach

        result = self.app.get(f'/coach/{sample_coach_id}')
        self.assertEqual(result.status, '200 OK')
        
    # @mock.patch('pymongo.collection.Collection.insert_one')
    # def test_submit_playlist(self, mock_insert):
    #     """Test submitting a new coach."""
    #     result = self.app.post('/coaches', data=sample_form_data)
    #     # After submitting, should redirect to that playlist's page
    #     self.assertEqual(result.status, '302 FOUND')
    #     mock_insert.assert_called_with(sample_coach)

    # Testing Routes
    def test_index(self):
        """Test the app's homepage."""
        result = self.app.get('/')
        self.assertEqual(result.status, '200 OK')
        
    def test_login(self):
        """Test the app's login page."""
        result = self.app.get('/login')
        self.assertEqual(result.status, '200 OK')
        
    def test_index(self):
        """Test the app's coaches index page."""
        result = self.app.get('/')
        self.assertEqual(result.status, '200 OK')
        
    def test_coaches_submit(self):
        """Test the app's coach submit page."""
        result = self.app.get('/coaches')
        self.assertEqual(result.status, '200 OK')
        
    def test_coaches_new(self):
        """Test the app's create new coach page."""
        result = self.app.get('/coaches/new')
        self.assertEqual(result.status, '200 OK')
        
    def test_coaches_show(self):
        """Test the app's show all coaches page."""
        result = self.app.get('/coaches')
        self.assertEqual(result.status, '200 OK')
        
    # def test_coach_reviews_new(self):
    #     """Test the app's create a review page."""
    #     result = self.app.get('/coaches/{reviews}')
    #     self.assertEqual(result.status, '200 OK')
    
    def test_leagues_show(self):
        """Test the app's show all leagues page."""
        result = self.app.get('/leagues')
        self.assertEqual(result.status, '200 OK')
        
    def test_leagues_new(self):
        """Test the app's create a new league page."""
        result = self.app.get('/leagues/new')
        self.assertEqual(result.status, '200 OK')
        
    # def test_leagues_delete(self):
    #     """Test the app's delete a leagues page."""
    #     result = self.app.get('/leagues/{league_id}/delete')
    #     self.assertEqual(result.status, '200 OK')
        
    def test_fields_show(self):
        """Test the app's show all fields page."""
        result = self.app.get('/fields')
        self.assertEqual(result.status, '200 OK')
        
    def test_fields_new(self):
        """Test the app's create a new field page."""
        result = self.app.get('/fields/new')
        self.assertEqual(result.status, '200 OK')