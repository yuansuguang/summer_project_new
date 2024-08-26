from django.test import TestCase
from survey.models import *
from django.utils import timezone

class SurveyModelTestCase(TestCase):
    def setUp(self):
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            is_available=True,
            last_modified_time=timezone.now()
        )

    def test_survey_creation(self):
        self.assertEqual(self.survey.survey_title, 'Test Survey')
        self.assertEqual(self.survey.username, 'test_user')
        self.assertTrue(self.survey.is_available)

    def test_survey_update(self):
        self.survey.survey_title = 'Updated Survey Title'
        self.survey.save()
        self.assertEqual(self.survey.survey_title, 'Updated Survey Title')

    def test_survey_deletion(self):
        survey_id = self.survey.survey_id
        self.survey.delete()
        with self.assertRaises(Survey.DoesNotExist):
            Survey.objects.get(survey_id=survey_id)

class QuestionModelTestCase(TestCase):
    def setUp(self):
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            is_available=True,
            last_modified_time=timezone.now()
        )
        self.question = Question.objects.create(
            survey_id=self.survey,
            question_title='Test Question',
            question_description='This is a test question',
            question_type='radio',
            sequence_id=1
        )

    def test_question_creation(self):
        self.assertEqual(self.question.question_title, 'Test Question')
        self.assertEqual(self.question.survey_id, self.survey)

    def test_question_update(self):
        self.question.question_title = 'Updated Question Title'
        self.question.save()
        self.assertEqual(self.question.question_title, 'Updated Question Title')

    def test_question_deletion(self):
        question_id = self.question.question_id
        self.question.delete()
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(question_id=question_id)

class OptionModelTestCase(TestCase):
    def setUp(self):
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            is_available=True,
            last_modified_time=timezone.now()
        )
        self.question = Question.objects.create(
            survey_id=self.survey,
            question_title='Test Question',
            question_description='This is a test question',
            question_type='radio',
            sequence_id=1
        )
        self.option = Option.objects.create(
            question_id=self.question,
            option_description='Test Option',
            sequence_id=1
        )

    def test_option_creation(self):
        self.assertEqual(self.option.option_description, 'Test Option')
        self.assertEqual(self.option.question_id, self.question)

    def test_option_update(self):
        self.option.option_description = 'Updated Option Description'
        self.option.save()
        self.assertEqual(self.option.option_description, 'Updated Option Description')

    def test_option_deletion(self):
        option_id = self.option.option_id
        self.option.delete()
        with self.assertRaises(Option.DoesNotExist):
            Option.objects.get(option_id=option_id)

class SurveySubmitModelTestCase(TestCase):
    def setUp(self):
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            is_available=True,
            last_modified_time=timezone.now()
        )
        self.survey_submit = Survey_submit.objects.create(
            survey_id=self.survey,
            username='test_user'
        )

    def test_survey_submit_creation(self):
        self.assertEqual(self.survey_submit.survey_id, self.survey)
        self.assertEqual(self.survey_submit.username, 'test_user')

    def test_survey_submit_update(self):
        self.survey_submit.survey_score = 80
        self.survey_submit.save()
        self.assertEqual(self.survey_submit.survey_score, 80)

    def test_survey_submit_deletion(self):
        survey_submit_id = self.survey_submit.survey_submit_id
        self.survey_submit.delete()
        with self.assertRaises(Survey_submit.DoesNotExist):
            Survey_submit.objects.get(survey_submit_id=survey_submit_id)

class QuestionSubmitModelTestCase(TestCase):
    def setUp(self):
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            is_available=True,
            last_modified_time=timezone.now()
        )
        self.question = Question.objects.create(
            survey_id=self.survey,
            question_title='Test Question',
            question_description='This is a test question',
            question_type='radio',
            sequence_id=1
        )
        self.survey_submit = Survey_submit.objects.create(
            survey_id=self.survey,
            username='test_user'
        )
        self.question_submit = Question_submit.objects.create(
            question_id=self.question,
            survey_submit_id=self.survey_submit,
            answer='Test Answer',
            username='test_user'
        )

    def test_question_submit_creation(self):
        self.assertEqual(self.question_submit.question_id, self.question)
        self.assertEqual(self.question_submit.survey_submit_id, self.survey_submit)
        self.assertEqual(self.question_submit.answer, 'Test Answer')

    def test_question_submit_update(self):
        self.question_submit.answer = 'Updated Answer'
        self.question_submit.save()
        self.assertEqual(self.question_submit.answer, 'Updated Answer')

    def test_question_submit_deletion(self):
        question_submit_id = self.question_submit.question_submit_id
        self.question_submit.delete()
        with self.assertRaises(Question_submit.DoesNotExist):
            Question_submit.objects.get(question_submit_id=question_submit_id)
