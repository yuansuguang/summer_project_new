from django.test import SimpleTestCase
from submit.form import clear_survey_submit_form, clear_single_submit_form

class TestForms(SimpleTestCase):

    def test_clear_survey_submit_form_valid_data(self):
        form = clear_survey_submit_form(data={
            'survey_id': 1
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['survey_id'], 1)

    def test_clear_survey_submit_form_invalid_data(self):
        form = clear_survey_submit_form(data={})

        self.assertFalse(form.is_valid())
        self.assertIn('survey_id', form.errors)

    def test_clear_single_submit_form_valid_data(self):
        form = clear_single_submit_form(data={
            'submit_id': 1
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['submit_id'], 1)

    def test_clear_single_submit_form_invalid_data(self):
        form = clear_single_submit_form(data={})

        self.assertFalse(form.is_valid())
        self.assertIn('submit_id', form.errors)
