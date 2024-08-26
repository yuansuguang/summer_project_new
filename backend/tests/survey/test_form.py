from django.test import TestCase
from survey.form import *

class SurveyFormsTestCase(TestCase):

    def test_list_survey_form_valid_data(self):
        form_data = {
            'survey_keyword': 'Test Survey',
            'is_deleted': False,
            'is_collected': True,
            'is_released': 1,
            'survey_type': 'type1',
            'sort_key': 'date',
            'sort_type': 'asc',
            'username': 'testuser',
        }
        form = list_survey_form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_list_survey_form_empty_data(self):
        form_data = {}
        form = list_survey_form(data=form_data)
        self.assertTrue(form.is_valid())  
        
    def test_list_survey_form_invalid_data(self):
        form_data = {
            'is_released': 'invalid', 
        }
        form = list_survey_form(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('is_released', form.errors)

    def test_share_survey_form_valid_data(self):
        form_data = {
            'survey_id': 123,
        }
        form = share_survey_form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_share_survey_form_missing_survey_id(self):
        form_data = {}
        form = share_survey_form(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('survey_id', form.errors) 
