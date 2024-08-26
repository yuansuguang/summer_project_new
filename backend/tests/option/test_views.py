import json
from django.test import TestCase, RequestFactory
from survey.models import Question, Survey, Option  # Survey 및 Question 모델 임포트
from option.views import *  # 뷰 함수 임포트
from option.form import create_option_form  # 테스트 시에 폼이 필요함
from django.utils import timezone
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore

class ChangeOptionDescriptionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        
        # Survey와 Question 객체 생성
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            last_modified_time=timezone.now()
        )
        self.question = Question.objects.create(
            question_title='Test Question',
            survey_id=self.survey,
            question_type='text'
        )

        # Option 객체 생성
        self.option = Option.objects.create(
            option_description='Initial description',
            question_id=self.question,
            sequence_id=1
        )

    def add_session_to_request(self, request):
        """세션을 테스트 요청에 추가"""
        middleware = SessionMiddleware(get_response=lambda x: x)
        middleware.process_request(request)
        request.session.save()

    def test_change_option_description_success(self):
        request = self.factory.post('/change-option-description/', {
            'option_id': self.option.option_id,
            'new_description': 'Updated description'
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = change_option_description(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)
        self.option.refresh_from_db()
        self.assertEqual(self.option.option_description, 'Updated description')

    def test_change_option_description_missing_parameters(self):
        request = self.factory.post('/change-option-description/', {
            'option_id': self.option.option_id,
            # 'new_description' 누락
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = change_option_description(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 2)
        self.assertEqual(response_data['message'], 'Missing required parameters.')

    def test_change_option_description_not_logged_in(self):
        request = self.factory.post('/change-option-description/', {
            'option_id': self.option.option_id,
            'new_description': 'Updated description'
        })
        self.add_session_to_request(request)  # 세션 추가하지만 로그인 상태는 아님

        response = change_option_description(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 401)

    def test_change_option_description_option_not_found(self):
        request = self.factory.post('/change-option-description/', {
            'option_id': 999,  # 존재하지 않는 ID
            'new_description': 'Updated description'
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = change_option_description(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 3)
        self.assertEqual(response_data['message'], 'Option does not exist.')
