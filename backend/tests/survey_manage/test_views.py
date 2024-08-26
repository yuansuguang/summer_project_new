from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from django.contrib.sessions.middleware import SessionMiddleware
from survey_manage.views import *
from survey.models import Survey, Question, Option
from django.utils import timezone
import json
import datetime


class SurveyManageTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'test_user'
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username=self.username,
            is_available=True,
            last_modified_time=timezone.now(),
            question_num=1
        )

    def add_session_to_request(self, request):
        middleware = SessionMiddleware(get_response=lambda req: None)
        middleware.process_request(request)
        request.session.save()
        request.session['is_login'] = True
        request.session['username'] = self.username

    def test_survey_create_no_login(self):
        request = self.factory.post('/api/survey_create', {})
        self.add_session_to_request(request)  
        request.session['is_login'] = False 
        
        response = survey_create(request)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status_code'], 401)

    def test_survey_create_success(self):
        request = self.factory.post('/api/survey_create', {
            'title': 'New Survey',
            'description': 'Survey description',
            'type': '1'
        })
        self.add_session_to_request(request)

        response = survey_create(request)
        response_data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)
        self.assertTrue(Survey.objects.filter(survey_id=response_data['survey_id']).exists())

    def test_remove_to_recycle_no_login(self):
        request = self.factory.post('/api/remove_to_recycle', {'survey_id': self.survey.survey_id})
        self.add_session_to_request(request) 
        request.session['is_login'] = False   
        
        response = remove_to_recycle(request)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status_code'], 401)

    def test_remove_to_recycle_success(self):
        request = self.factory.post('/api/remove_to_recycle', {'survey_id': self.survey.survey_id})
        self.add_session_to_request(request)

        response = remove_to_recycle(request)
        response_data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)
        self.survey.refresh_from_db()
        self.assertTrue(self.survey.is_deleted)

    def test_delete_survey_no_login(self):
        request = self.factory.post('/api/delete_survey', {'survey_id': self.survey.survey_id})
        self.add_session_to_request(request)  
        request.session['is_login'] = False   
        
        response = delete_survey(request)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status_code'], 401)

    def test_delete_survey_success(self):
        request = self.factory.post('/api/delete_survey', {'survey_id': self.survey.survey_id})
        self.add_session_to_request(request)

        response = delete_survey(request)
        response_data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)
        self.assertFalse(Survey.objects.filter(survey_id=self.survey.survey_id).exists())

class SurveyManageViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'test_user'
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey.',
            username=self.username,
            is_available=False,
            is_deleted=True,
            is_collected=False,
            last_modified_time=timezone.now(),
            question_num=0
        )

    def add_session_to_request(self, request):
        middleware = SessionMiddleware(get_response=lambda req: None)
        middleware.process_request(request)
        request.session.save()
        request.session['is_login'] = True
        request.session['username'] = self.username

    def test_survey_recover_success(self):
        request = self.factory.post('/api/survey_recover/', data={'survey_id': self.survey.survey_id})
        self.add_session_to_request(request)

        response = survey_recover(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)

        self.survey.refresh_from_db()
        self.assertFalse(self.survey.is_deleted)

    def test_survey_collect_success(self):
        request = self.factory.post('/api/survey_collect/', data={'survey_id': self.survey.survey_id})
        self.add_session_to_request(request)

        response = survey_collect(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)

        self.survey.refresh_from_db()
        self.assertTrue(self.survey.is_collected)

    def test_publish_survey_success(self):
        request = self.factory.post('/api/publish_survey/', data={'survey_id': self.survey.survey_id})
        self.add_session_to_request(request)

        response = publish_survey(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)

        self.survey.refresh_from_db()
        self.assertTrue(self.survey.is_available)

    def test_close_survey_success(self):
        self.survey.is_available = True
        self.survey.save()

        request = self.factory.post('/api/close_survey/', data={'survey_id': self.survey.survey_id})
        self.add_session_to_request(request)

        response = close_survey(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)

        self.survey.refresh_from_db()
        self.assertFalse(self.survey.is_available)

    def test_open_or_close_survey_success(self):
        request = self.factory.post('/api/open_or_close_survey/', data={'survey_id': self.survey.survey_id})
        self.add_session_to_request(request)

        response = open_or_close_survey(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)

        self.survey.refresh_from_db()
        self.assertTrue(self.survey.is_available)

        response = open_or_close_survey(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)

        self.survey.refresh_from_db()
        self.assertFalse(self.survey.is_available)

class SurveyManagementTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.username = 'test_user'
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey.',
            username=self.username,
            is_available=True,
            is_deleted=False,
            last_modified_time=timezone.now(),
            deadline=timezone.now() + datetime.timedelta(days=5),
            duration=60,
            max_submission=100,
            question_num=3
        )
        self.question = Question.objects.create(
            survey_id=self.survey,
            question_title="Sample Question",
            question_description="This is a sample question.",
            sequence_id=1,
            question_type="radio"
        )
        self.option = Option.objects.create(
            question_id=self.question,
            option_description="Sample Option",
            sequence_id=1
        )

    def add_session_to_request(self, request):
        middleware = SessionMiddleware(get_response=lambda req: None)
        middleware.process_request(request)
        request.session.save()
        request.session['is_login'] = True
        request.session['username'] = self.username

    def test_update_survey_deadline_success(self):
        request = self.factory.post('/api/update_survey_deadline/', data={
            'survey_id': self.survey.survey_id,
            'new_deadline': (timezone.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M')
        })
        self.add_session_to_request(request)

        response = update_survey_deadline(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)

    def test_update_survey_duration_success(self):
        request = self.factory.post('/api/update_survey_duration/', data={
            'survey_id': self.survey.survey_id,
            'new_duration': 120
        })
        self.add_session_to_request(request)

        response = update_survey_duration(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)

    def test_update_survey_max_submission_success(self):
        request = self.factory.post('/api/update_survey_max_submission/', data={
            'survey_id': self.survey.survey_id,
            'new_max_submission': 200
        })
        self.add_session_to_request(request)

        response = update_survey_max_submission(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)

    def test_duplicate_survey_success(self):
        request = self.factory.post('/api/duplicate_survey/', data={
            'survey_id': self.survey.survey_id
        })
        self.add_session_to_request(request)

        response = duplicate_survey(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)
        self.assertNotEqual(response_data['new_survey_id'], self.survey.survey_id)

    def test_save_entire_survey_success(self):
        survey_data = {
            "qn_id": self.survey.survey_id,
            "title": "Updated Survey Title",
            "description": "Updated Survey Description",
            "finished_time": "2024-08-22 12:00",
            "questions": [
                {
                    "question_id": self.question.question_id,
                    "title": "Updated Question",
                    "description": "Updated Question Description",  
                    "type": "radio", 
                    "must": True,
                    "id": 3, 
                    "options": [
                        {"id": self.option.option_id,
                        "title": "Updated Option", 
                        "sequence_id": 1}
                    ]
                }
            ]
        }
        request = self.factory.post('/api/save_entire_survey/', data=json.dumps(survey_data), content_type='application/json')
        self.add_session_to_request(request)

        response = save_entire_survey(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status_code'], 1)

class SaveSurveyUtilTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.survey = Survey.objects.create(
            survey_title="Test Survey",
            survey_description="This is a test survey.",
            username="test_user",
            create_time=timezone.now(),
            last_modified_time=timezone.now(),
            is_available=True,
            survey_type="1"
        )
        self.question = Question.objects.create(
            survey_id=self.survey,
            question_title="Test Question",
            question_description="This is a test question.",
            question_type="radio",
            is_necessary=True,
            sequence_id=1
        )
        self.option = Option.objects.create(
            question_id=self.question,
            option_description="Test Option",
            sequence_id=1
        )

    def test_save_survey_util_update_existing_question(self):
        survey_data = {
            "title": "Updated Survey Title",
            "description": "Updated Survey Description",
            "finished_time": "2024-08-22 12:00",
            "questions": [
                {
                    "question_id": self.question.question_id,
                    "title": "Updated Question",
                    "description": "Updated Question Description",
                    "type": "checkbox",
                    "must": True,
                    "id": self.question.sequence_id,
                    "options": [
                        {
                            "id": self.option.sequence_id,
                            "title": "Updated Option"
                        }
                    ]
                }
            ]
        }
        save_survey_util(survey_data, self.survey.survey_id)
        
        self.survey.refresh_from_db()
        self.question.refresh_from_db()
        
        updated_option = Option.objects.get(question_id=self.question, sequence_id=self.option.sequence_id)

        self.assertEqual(self.survey.survey_title, "Updated Survey Title")
        self.assertEqual(self.question.question_title, "Updated Question")
        self.assertEqual(updated_option.option_description, "Updated Option")

    def test_save_survey_util_add_new_question(self):
        #새로운 질문을 추가하는 시나리오를 테스트
        survey_data = {
            "title": "Updated Survey Title",
            "description": "Updated Survey Description",
            "finished_time": "2024-08-22 12:00",
            "questions": [
                {
                    "question_id": self.question.question_id,
                    "title": "Updated Question",
                    "description": "Updated Question Description",
                    "type": "checkbox",
                    "must": True,
                    "id": self.question.sequence_id,
                    "options": [
                        {
                            "id": self.option.sequence_id,
                            "title": "Updated Option"
                        }
                    ]
                },
                {
                    "question_id": 999, 
                    "title": "New Question",
                    "description": "New Question Description",
                    "type": "text",
                    "must": False,
                    "id": 2,
                    "options": []
                }
            ]
        }
        save_survey_util(survey_data, self.survey.survey_id)
        
        self.survey.refresh_from_db()
        new_question = Question.objects.get(question_title="New Question")

        self.assertEqual(self.survey.survey_title, "Updated Survey Title")
        self.assertEqual(new_question.question_title, "New Question")
        self.assertEqual(new_question.question_description, "New Question Description")

    def test_save_survey_util_remove_question(self):
    
        survey_data = {
            "title": "Updated Survey Title",
            "description": "Updated Survey Description",
            "finished_time": "2024-08-22 12:00",
            "questions": []  
        }
        save_survey_util(survey_data, self.survey.survey_id)
        
        self.survey.refresh_from_db()
        questions_count = Question.objects.filter(survey_id=self.survey.survey_id).count()

        self.assertEqual(questions_count, 0) 








