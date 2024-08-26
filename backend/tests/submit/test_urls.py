from django.test import SimpleTestCase
from django.urls import reverse, resolve
from submit.views import *


class TestSubmitUrls(SimpleTestCase):

    def test_submit_survey_url_is_resolved(self):
        url = reverse('submit_survey')
        self.assertEqual(resolve(url).func, submit_survey)

    def test_save_survey_url_is_resolved(self):
        url = reverse('save_survey')
        self.assertEqual(resolve(url).func, save_survey)

    def test_clear_survey_url_is_resolved(self):
        url = reverse('clear_survey')
        self.assertEqual(resolve(url).func, clear_survey)

    def test_get_submissions_by_question_id_url_is_resolved(self):
        url = reverse('get_submissions_by_question_id')
        self.assertEqual(resolve(url).func, get_submissions_by_question_id)

    def test_get_question_statistics_url_is_resolved(self):
        url = reverse('get_question_statistics')
        self.assertEqual(resolve(url).func, get_question_statistics)

    def test_get_survey_submissions_url_is_resolved(self):
        url = reverse('get_survey_submissions')
        self.assertEqual(resolve(url).func, get_survey_submissions)

    def test_get_user_submissions_url_is_resolved(self):
        url = reverse('get_user_submissions')
        self.assertEqual(resolve(url).func, get_user_submissions)

    def test_delete_submission_url_is_resolved(self):
        url = reverse('delete_submission')
        self.assertEqual(resolve(url).func, delete_submission)
