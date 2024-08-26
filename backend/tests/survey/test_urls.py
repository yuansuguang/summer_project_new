from django.test import TestCase, Client
from django.urls import reverse

class URLTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_survey_list_url_with_login(self):
        url = reverse('survey_list')
        session = self.client.session
        session['is_login'] = True  
        session.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  

    def test_survey_share_url_with_login(self):
        url = reverse('survey_share')
        session = self.client.session
        session['is_login'] = True  
        session.save()
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)  

    def test_survey_link_url_with_login(self):
        url = reverse('survey_link')
        session = self.client.session
        session['is_login'] = True  
        session.save()
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)  
