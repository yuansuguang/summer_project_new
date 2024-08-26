from django.test import TestCase
from option.form import create_option_form

class CreateOptionFormTest(TestCase):

    def test_create_option_form_valid(self):
        form_data = {
            'description': 'This is a valid description.',
            'question_id': 1,
            'sequence_id': 1,
        }
        form = create_option_form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_option_form_invalid_description_length(self):
        # 긴거
        form_data = {
            'description': 'a' * 251,
            'question_id': 1,
            'sequence_id': 1,
        }
        form = create_option_form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_option_form_missing_description(self):
        # 설명없
        form_data = {
            'question_id': 1,
            'sequence_id': 1,
        }
        form = create_option_form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_option_form_invalid_question_id(self):
        # question_id 문자
        form_data = {
            'description': 'This is a valid description.',
            'question_id': 'invalid', 
            'sequence_id': 1,
        }
        form = create_option_form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_option_form_missing_fields(self):
        # 값없
        form_data = {}
        form = create_option_form(data=form_data)
        self.assertFalse(form.is_valid())


#해결