from django.test import SimpleTestCase
from django.urls import reverse, resolve
from question.views import *

class TestQuestionUrls(SimpleTestCase):

    def test_list_question_url_is_resolved(self):
        url = reverse('list_question')
        self.assertEqual(resolve(url).func, list_question)

    def test_list_question_forfill_url_is_resolved(self):
        url = reverse('list_question_forfill')
        self.assertEqual(resolve(url).func, list_question_forfill)

    def test_list_question_alt_url_is_resolved(self):
        url = reverse('list_question_alt')
        self.assertEqual(resolve(url).func, list_question_alt)

    def test_list_question_forpreview_url_is_resolved(self):
        url = reverse('list_question_forpreview')
        self.assertEqual(resolve(url).func, list_question_forpreview)

    def test_list_question_foranalysis_url_is_resolved(self):
        url = reverse('list_question_foranalysis')
        self.assertEqual(resolve(url).func, list_question_foranalysis)
