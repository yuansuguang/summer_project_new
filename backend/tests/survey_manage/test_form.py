from django.test import TestCase
from submit.form import *

class ClearSurveySubmitFormTest(TestCase):
    def test_clear_survey_submit_form_valid(self):
        form_data = {'survey_id': 1}
        form = clear_survey_submit_form(data=form_data)
        self.assertTrue(form.is_valid()) 

    def test_clear_survey_submit_form_invalid(self):
        form_data = {'survey_id': 'invalid'}
        form = clear_survey_submit_form(data=form_data)
        self.assertFalse(form.is_valid())  
        self.assertIn('survey_id', form.errors)  

class ClearSingleSubmitFormTest(TestCase):
    def test_clear_single_submit_form_valid(self):
        form_data = {'submit_id': 1}
        form = clear_single_submit_form(data=form_data)
        self.assertTrue(form.is_valid())  

    def test_clear_single_submit_form_invalid(self):
        form_data = {'submit_id': 'invalid'}
        form = clear_single_submit_form(data=form_data)
        self.assertFalse(form.is_valid())  
        self.assertIn('submit_id', form.errors)  