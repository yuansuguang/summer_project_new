from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils import timezone
from django.urls import reverse
from survey.models import Survey
from survey.views import *
import json

class SurveyListTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('survey_list')
        self.user_session_data = {'is_login': True, 'username': 'testuser'}

    
        self.survey1 = Survey.objects.create(
            survey_title='Survey 1',
            survey_description='Description 1',
            username='testuser',
            is_available=True,
            is_deleted=False,
            is_collected=True,
            survey_type='1',  # 普通问卷
            submission_num=10,
            question_num=5,
            create_time=timezone.now(),
            last_modified_time=timezone.now()
        )

        self.survey2 = Survey.objects.create(
            survey_title='Survey 2',
            survey_description='Description 2',
            username='testuser',
            is_available=True,
            is_deleted=False,
            is_collected=True,
            survey_type='2',  # 投票问卷
            submission_num=5,
            question_num=3,
            create_time=timezone.now(),
            last_modified_time=timezone.now()
        )

        #데이터베이스에 Survey 객체가 두 개 있는지 확인
        self.assertEqual(Survey.objects.count(), 2)

    def add_session_to_request(self, request):
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.update(self.user_session_data)
        request.session.save()

    def test_survey_list_view_success(self):
        request = self.factory.post(self.url, data={})
        self.add_session_to_request(request)
        response = survey_list(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)
        self.assertEqual(len(json.loads(response_data['data'])), 2)  

    def test_survey_list_with_filter(self):
        request = self.factory.post(self.url, data={'survey_keyword': 'Survey 1'})
        self.add_session_to_request(request)
        response = survey_list(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)
        self.assertEqual(len(json.loads(response_data['data'])), 1)
        self.assertEqual(json.loads(response_data['data'])[0]['questionnaireName'], 'Survey 1')

    def test_survey_list_invalid_form(self):
        request = self.factory.post(self.url, data={'is_released': 'invalid'})
        self.add_session_to_request(request)
        response = survey_list(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 4)

    def test_survey_list_no_login(self):
        request = self.factory.post(self.url, data={})
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        response = survey_list(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 401)

    def test_survey_list_method_not_allowed(self):
        request = self.factory.get(self.url)
        self.add_session_to_request(request)
        response = survey_list(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 3)

class SurveyShareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('survey_share')
        self.user_session_data = {'is_login': True, 'username': 'testuser'}

        self.survey = Survey.objects.create(
            survey_title='Survey 1',
            survey_description='Description 1',
            username='testuser',
            is_available=False,  #공유 전에는 사용 불가
            share_code=None,
            submission_num=0,
            question_num=5,
            create_time=timezone.now(),
            last_modified_time=timezone.now()
        )

    def add_session_to_request(self, request):
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.update(self.user_session_data)
        request.session.save()

    def test_survey_share_success(self):
        request = self.factory.post(self.url, data={'survey_id': self.survey.survey_id})
        self.add_session_to_request(request) 
        response = survey_share(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)
        self.assertIsNotNone(response_data['code'])  

        self.survey.refresh_from_db()
        self.assertTrue(self.survey.is_available)
        self.assertEqual(self.survey.share_code, response_data['code'])

    def test_survey_share_no_login(self):
        request = self.factory.post(self.url, data={'survey_id': self.survey.survey_id})
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        response = survey_share(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 401)

    def test_survey_share_invalid_form(self):
        request = self.factory.post(self.url, data={})
        self.add_session_to_request(request)  
        response = survey_share(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 3)
        self.assertEqual(response_data['message'], 'invalid form')

    def test_survey_share_survey_not_exists(self):
        request = self.factory.post(self.url, data={'survey_id': 9999})  
        self.add_session_to_request(request) 
        response = survey_share(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 2)
        self.assertEqual(response_data['message'], 'survey not exists')

    def test_survey_share_method_not_allowed(self):
        request = self.factory.get(self.url)  
        self.add_session_to_request(request) 
        response = survey_share(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 4)
        self.assertEqual(response_data['message'], 'method error')

class SurveyLinkTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('survey_link')
        self.user_session_data = {'is_login': True, 'username': 'testuser'}

        self.survey = Survey.objects.create(
            survey_title='Survey 1',
            survey_description='Description 1',
            username='testuser',
            is_available=True,  #공유 가능
            share_code='testcode123',
            submission_num=0,
            question_num=5,
            create_time=timezone.now(),
            last_modified_time=timezone.now()
        )

    def add_session_to_request(self, request):
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.update(self.user_session_data)
        request.session.save()

    def test_survey_link_success(self):
        request = self.factory.post(self.url, data={'survey_id': self.survey.survey_id})
        self.add_session_to_request(request)  #세션 추가
        response = survey_link(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)
        self.assertEqual(response_data['code'], self.survey.share_code)

    def test_survey_link_no_login(self):
        request = self.factory.post(self.url, data={'survey_id': self.survey.survey_id})
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        response = survey_link(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 401)

    def test_survey_link_invalid_form(self):
        request = self.factory.post(self.url, data={})
        self.add_session_to_request(request)  #세션 추가
        response = survey_link(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 3)
        self.assertEqual(response_data['message'], 'invalid form')

    def test_survey_link_survey_not_exists(self):
        request = self.factory.post(self.url, data={'survey_id': 9999})  
        self.add_session_to_request(request)  
        response = survey_link(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 2)
        self.assertEqual(response_data['message'], 'survey not exists')

    def test_survey_link_survey_not_available(self):
        self.survey.is_available = False
        self.survey.save()

        request = self.factory.post(self.url, data={'survey_id': self.survey.survey_id})
        self.add_session_to_request(request) 
        response = survey_link(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 5)
        self.assertEqual(response_data['message'], 'not available')

    def test_survey_link_method_not_allowed(self):
        request = self.factory.get(self.url)  
        self.add_session_to_request(request) 
        response = survey_link(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 4)
        self.assertEqual(response_data['message'], 'method error')



