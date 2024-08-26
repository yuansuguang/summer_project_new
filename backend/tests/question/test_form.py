from django.test import TestCase
from question.form import *

class FormValidationTestCase(TestCase):
    
    def test_create_question_form_valid_data(self):
        form_data = {
            'title': 'Sample Title',
            'description': 'Sample Description',
            'type': 'text',
            'survey_id': 1,
            'sequence_id': 1
        }
        form = create_question_form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_question_form_missing_data(self):
        form_data = {
            'title': 'Sample Title',
            'description': 'Sample Description',
            #'type'가 누락된 경우
            'survey_id': 1,
            'sequence_id': 1
        }
        form = create_question_form(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('type', form.errors)

    def test_change_question_sequence_form_valid_data(self):
        form_data = {
            'question_id': 1,
            'cur_sequence_id': 2
        }
        form = change_question_sequence_form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_change_question_sequence_form_missing_data(self):
        form_data = {
            'question_id': 1,
            #'cur_sequence_id'가 누락된 경우
        }
        form = change_question_sequence_form(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cur_sequence_id', form.errors)

    def test_list_question_form_valid_data(self):
        form_data = {
            'survey_id': 1
        }
        form = list_question_form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_list_question_forfill_form_valid_data(self):
        form_data = {
            'code': 'sample_code'
        }
        form = list_question_forfill_form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_list_question_forpreview_form_valid_data(self):
        form_data = {
            'survey_id': 1
        }
        form = list_question_forpreview_form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_list_question_forpreview_form_missing_data(self):
        form_data = {
            #'survey_id'가 누락된 경우
        }
        form = list_question_forpreview_form(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('survey_id', form.errors)

