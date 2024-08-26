import json
from unittest import mock
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.contrib.sessions.backends.db import SessionStore
from survey.models import Survey, Question, Option
from question.views import *

class ListQuestionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            last_modified_time=timezone.now()
        )

        self.question = Question.objects.create(
            question_title='Test Question',
            question_description='Test Question Description',
            survey_id=self.survey,
            question_type='radio',
            sequence_id=1,
            is_necessary=True,
            is_hidden=False,
            option_num=2,
            score=5,
            max_point=10,
            correct_answer='Correct Answer',
            image_url='http://example.com/image1.jpg-<^-^>-http://example.com/image2.jpg'
        )

        self.option1 = Option.objects.create(
            option_description='Option 1',
            question_id=self.question,
            sequence_id=1
        )

        self.option2 = Option.objects.create(
            option_description='Option 2',
            question_id=self.question,
            sequence_id=2
        )

    def add_session_to_request(self, request):
        session = SessionStore()
        session.create()
        request.session = session

    def test_list_question_success(self):
        request = self.factory.post('/list-question/', data={
            'survey_id': self.survey.survey_id
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 1)

        data = json.loads(response_data.get('data'))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['question_id'], self.question.question_id)
        self.assertEqual(len(data[0]['options']), 2)
        self.assertEqual(data[0]['options'][0]['title'], 'Option 1')
        self.assertEqual(data[0]['options'][1]['title'], 'Option 2')
        
        # imgList의 길이를 1로 예상하고 검증
        self.assertEqual(len(data[0]['imgList']), 1)
        self.assertEqual(data[0]['imgList'][0]['url'], 'http://example.com/image1.jpg')

    def test_list_question_not_logged_in(self):
        request = self.factory.post('/list-question/', data={
            'survey_id': self.survey.survey_id
        })
        self.add_session_to_request(request)

        response = list_question(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 401)

    def test_list_question_invalid_method(self):
        request = self.factory.get('/list-question/')
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 3)

    def test_list_question_invalid_form(self):
        request = self.factory.post('/list-question/', data={})
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 2)

class ListQuestionForAnalysisTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            last_modified_time=timezone.now()
        )

        # 라디오 타입 질문 생성
        self.radio_question = Question.objects.create(
            question_title='Radio Question',
            question_description='Radio Question Description',
            survey_id=self.survey,
            question_type='radio',
            sequence_id=1,
            is_necessary=True,
            is_hidden=False,
            option_num=2,
            score=5,
            max_point=10,
            correct_answer='Correct Answer'
        )

        # 체크박스 타입 질문 생성
        self.checkbox_question = Question.objects.create(
            question_title='Checkbox Question',
            question_description='Checkbox Question Description',
            survey_id=self.survey,
            question_type='checkbox',
            sequence_id=2,
            is_necessary=True,
            is_hidden=False,
            option_num=2,
            score=5,
            max_point=10,
            correct_answer='Correct Answer'
        )

        # Option 객체 생성
        self.option1 = Option.objects.create(
            option_description='Option 1',
            question_id=self.radio_question,
            sequence_id=1
        )

        self.option2 = Option.objects.create(
            option_description='Option 2',
            question_id=self.checkbox_question,
            sequence_id=2
        )

    def add_session_to_request(self, request):
        session = SessionStore()
        session.create()
        request.session = session

    def test_list_question_foranalysis_success(self):
        request = self.factory.post('/list-question-foranalysis/', data={
            'survey_id': self.survey.survey_id
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_foranalysis(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 1)

        data = json.loads(response_data.get('data'))
        self.assertEqual(len(data), 2)  # 라디오와 체크박스 질문이 각각 하나씩 존재

    def test_list_question_foranalysis_not_logged_in(self):
        request = self.factory.post('/list-question-foranalysis/', data={
            'survey_id': self.survey.survey_id
        })
        self.add_session_to_request(request)

        response = list_question_foranalysis(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 401)

    def test_list_question_foranalysis_invalid_method(self):
        request = self.factory.get('/list-question-foranalysis/')
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_foranalysis(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 3)

    def test_list_question_foranalysis_invalid_form(self):
        request = self.factory.post('/list-question-foranalysis/', data={})
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_foranalysis(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 2)

class ListQuestionAltTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            share_code='TESTCODE123',
            username='test_user',
            is_available=True,
            is_random=False,
            last_modified_time=timezone.now()
        )

        self.question = Question.objects.create(
            question_title='Test Question',
            question_description='Test Question Description',
            survey_id=self.survey,
            question_type='radio',
            sequence_id=1,
            is_necessary=True,
            is_hidden=False,
            option_num=2,
            score=5,
            max_point=10,
            correct_answer='Correct Answer',
            image_url='http://example.com/image1.jpg-<^-^>-http://example.com/image2.jpg'  # 유효한 URL 설정
        )

        self.option1 = Option.objects.create(
            option_description='Option 1',
            question_id=self.question,
            sequence_id=1
        )

        self.option2 = Option.objects.create(
            option_description='Option 2',
            question_id=self.question,
            sequence_id=2
        )

        self.survey_submit = Survey_submit.objects.create(
            survey_id=self.survey,
            username='test_user',
            is_submitted=True
        )

        self.question_submit = Question_submit.objects.create(
            question_id=self.question,
            survey_submit_id=self.survey_submit,
            answer='Option 1'
        )

    def add_session_to_request(self, request):
        session = SessionStore()
        session.create()
        request.session = session

    def test_list_question_alt_success_with_answers(self):
        request = self.factory.post('/list-question-alt/', data={
            'code': 'TESTCODE123'
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True
        request.session['username'] = 'test_user'

        response = list_question_alt(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 1)
        self.assertEqual(response_data.get('has_answers'), 1)

        data = json.loads(response_data.get('data'))
        self.assertEqual(len(data), 1)  # 하나의 질문이 있음
        self.assertEqual(data[0]['question_id'], self.question.question_id)
        self.assertEqual(data[0]['options'][0]['title'], 'Option 1')
        self.assertEqual(data[0]['options'][1]['title'], 'Option 2')

        answers = json.loads(response_data.get('answers'))
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0]['ans'], 'Option 1')

    def test_list_question_alt_success_without_answers(self):
        request = self.factory.post('/list-question-alt/', data={
            'code': 'TESTCODE123'
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True
        request.session['username'] = 'another_user'  # 다른 사용자로 설정

        response = list_question_alt(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 1)
        self.assertEqual(response_data.get('has_answers'), 0)

        data = json.loads(response_data.get('data'))
        self.assertEqual(len(data), 1)  # 하나의 질문이 있음
        self.assertEqual(data[0]['question_id'], self.question.question_id)
        self.assertEqual(data[0]['options'][0]['title'], 'Option 1')
        self.assertEqual(data[0]['options'][1]['title'], 'Option 2')

    def test_list_question_alt_survey_not_available(self):
        self.survey.is_available = False
        self.survey.save()

        request = self.factory.post('/list-question-alt/', data={
            'code': 'TESTCODE123'
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True
        request.session['username'] = 'test_user'

        response = list_question_alt(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 4)

    def test_list_question_alt_not_logged_in(self):
        request = self.factory.post('/list-question-alt/', data={
            'code': 'TESTCODE123'
        })
        self.add_session_to_request(request)

        response = list_question_alt(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 401)

    def test_list_question_alt_invalid_method(self):
        request = self.factory.get('/list-question-alt/')
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_alt(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 3)

    def test_list_question_alt_invalid_form(self):
        request = self.factory.post('/list-question-alt/', data={})
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_alt(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 2)

class ListQuestionForFillTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Survey 객체 생성
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            share_code='TESTCODE123',  # share_code가 올바르게 설정됨
            username='test_user',
            is_available=True,
            is_random=False,
            duration=30,
            last_modified_time=timezone.now(),
            survey_type='普通问卷'
        )

        self.question = Question.objects.create(
            question_title='Test Question',
            question_description='Test Question Description',
            survey_id=self.survey,
            question_type='radio',
            sequence_id=1,
            is_necessary=True,
            is_hidden=False,
            option_num=2,
            score=5,
            max_point=10,
            correct_answer='Correct Answer',
            image_url='http://example.com/image1.jpg-<^-^>-http://example.com/image2.jpg'
        )

        self.option1 = Option.objects.create(
            option_description='Option 1',
            question_id=self.question,
            sequence_id=1
        )

        self.option2 = Option.objects.create(
            option_description='Option 2',
            question_id=self.question,
            sequence_id=2
        )


    def add_session_to_request(self, request):
        session = SessionStore()
        session.create()
        request.session = session

    def test_list_question_forfill_success(self):
        # 데이터가 존재하는지 확인
        self.assertTrue(Survey.objects.filter(share_code='TESTCODE123').exists())

        request = self.factory.post('/list-question-forfill/', data={
            'code': 'TESTCODE123'
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_forfill(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 1)

        data = json.loads(response_data.get('data'))
        self.assertEqual(len(data), 1)  # 하나의 질문이 있음
        self.assertEqual(data[0]['question_id'], self.question.question_id)
        self.assertEqual(len(data[0]['options']), 2)
        self.assertEqual(data[0]['options'][0]['title'], 'Option 1')
        self.assertEqual(data[0]['options'][1]['title'], 'Option 2')

    def test_list_question_forfill_invalid_code(self):
        request = self.factory.post('/list-question-forfill/', data={
            'code': 'INVALIDCODE'  # 존재하지 않는 코드
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True

        try:
            response = list_question_forfill(request)
            response_data = json.loads(response.content)

            # Survey.DoesNotExist 예외가 발생하지 않는다면, 테스트를 실패로 처리합니다.
            self.fail("Expected Survey.DoesNotExist to be raised")

        except Survey.DoesNotExist:
            # 예외가 발생한 경우, 테스트는 성공합니다.
            pass


    def test_list_question_forfill_not_logged_in(self):
        request = self.factory.post('/list-question-forfill/', data={
            'code': 'TESTCODE123'
        })
        self.add_session_to_request(request)

        response = list_question_forfill(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 401)

    def test_list_question_forfill_invalid_method(self):
        request = self.factory.get('/list-question-forfill/')
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_forfill(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 3)

    def test_list_question_forfill_invalid_form(self):
        request = self.factory.post('/list-question-forfill/', data={})
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_forfill(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 2)

    def tearDown(self):
        Survey.objects.all().delete()
        Question.objects.all().delete()
        Option.objects.all().delete()

class ListQuestionForPreviewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            is_available=True,
            is_random=False,
            last_modified_time=timezone.now(),
            survey_type='普通问卷'
        )

        self.question = Question.objects.create(
            question_title='Test Question',
            question_description='Test Question Description',
            survey_id=self.survey,
            question_type='radio',
            sequence_id=1,
            is_necessary=True,
            is_hidden=False,
            option_num=2,
            score=5,
            max_point=10,
            correct_answer='Correct Answer',
            image_url='http://example.com/image1.jpg-<^-^>-http://example.com/image2.jpg'
        )

        self.option1 = Option.objects.create(
            option_description='Option 1',
            question_id=self.question,
            sequence_id=1
        )

        self.option2 = Option.objects.create(
            option_description='Option 2',
            question_id=self.question,
            sequence_id=2
        )

    def add_session_to_request(self, request):
        session = SessionStore()
        session.create()
        request.session = session

    def test_list_question_forpreview_success(self):
        request = self.factory.post('/list-question-forpreview/', data={
            'survey_id': self.survey.survey_id  # 올바른 survey_id 사용
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_forpreview(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 1)

        data = json.loads(response_data.get('data'))
        self.assertEqual(len(data), 1)  # 하나의 질문이 있음
        self.assertEqual(data[0]['question_id'], self.question.question_id)
        self.assertEqual(len(data[0]['options']), 2)
        self.assertEqual(data[0]['options'][0]['title'], 'Option 1')
        self.assertEqual(data[0]['options'][1]['title'], 'Option 2')

    def test_list_question_forpreview_invalid_survey_id(self):
        request = self.factory.post('/list-question-forpreview/', data={
            'survey_id': 99999  # 존재하지 않는 survey_id
        })
        self.add_session_to_request(request)
        request.session['is_login'] = True

        try:
            response = list_question_forpreview(request)
            response_data = json.loads(response.content)

            # Survey.DoesNotExist 예외가 발생하지 않는다면, 테스트를 실패로 처리합니다.
            self.fail("Expected Survey.DoesNotExist to be raised")

        except Survey.DoesNotExist:
            # 예외가 발생한 경우, 테스트는 성공합니다.
            pass

    def test_list_question_forpreview_not_logged_in(self):
        request = self.factory.post('/list-question-forpreview/', data={
            'survey_id': self.survey.survey_id
        })
        self.add_session_to_request(request)

        response = list_question_forpreview(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 401)

    def test_list_question_forpreview_invalid_method(self):
        request = self.factory.get('/list-question-forpreview/')
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_forpreview(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 3)

    def test_list_question_forpreview_invalid_form(self):
        request = self.factory.post('/list-question-forpreview/', data={})
        self.add_session_to_request(request)
        request.session['is_login'] = True

        response = list_question_forpreview(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('status_code'), 2)







