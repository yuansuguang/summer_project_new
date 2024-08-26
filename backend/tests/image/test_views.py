from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from survey.models import Survey, Question
from io import BytesIO
from PIL import Image
import os
import json
from django.utils import timezone
from django.conf import settings
from image.views import delete_image


class ImageUploadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            last_modified_time=timezone.now()  # 여기서 last_modified_time을 설정합니다.
        )
        self.question = Question.objects.create(
            question_title='Test Question',
            survey_id=self.survey,
            question_type='text'
        )

    def generate_test_image(self, format='JPEG'):
        # Helper function to generate a test image file
        image = Image.new('RGB', (100, 100))
        byte_io = BytesIO()
        image.save(byte_io, format)
        byte_io.seek(0)
        return byte_io

    def test_upload_image_success(self):
        image = self.generate_test_image()
        image.name = 'test_image.jpg'
        response = self.client.post(reverse('upload_image'), {
            'image': image,
        }, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status_code'], 1)

    def test_upload_image_invalid_form(self):
        response = self.client.post(reverse('upload_image'), {
            'wrong_field': 'invalid_data',
        }, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status_code'], 3)
        self.assertEqual(response.json()['message'], 'invalid form')

    def test_upload_image_invalid_method(self):
        response = self.client.get(reverse('upload_image'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status_code'], 4)
        self.assertEqual(response.json()['message'], 'invalid method')



class ImageDeleteTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()  # RequestFactory 인스턴스 생성
        self.survey = Survey.objects.create(
            survey_title='Test Survey',
            survey_description='This is a test survey',
            username='test_user',
            last_modified_time=timezone.now()
        )
        self.question = Question.objects.create(
            question_title='Test Question',
            survey_id=self.survey,
            image_url='test_image.jpg'
        )
        # 이미지 파일을 생성합니다.
        self.image_path = os.path.join(settings.MEDIA_ROOT, 'test_image.jpg')
        with open(self.image_path, 'wb') as f:
            f.write(b'Test image content')

    def test_delete_image_success(self):
        request = self.factory.post('/delete-image/', data={'question_id': self.question.question_id})
        response = delete_image(request)

        self.assertEqual(response.status_code, 200)
        
        # 응답 내용을 json.loads()로 파싱
        response_data = json.loads(response.content)
        
        self.assertEqual(response_data['success'], True)
        self.assertEqual(response_data['message'], 'Image deleted')
        self.assertFalse(os.path.exists(self.image_path))
        self.question.refresh_from_db()
        self.assertEqual(self.question.image_url, '')

    def test_delete_image_no_question_id(self):
        request = self.factory.post('/delete-image/')
        response = delete_image(request)

        self.assertEqual(response.status_code, 200)
        
        # 응답 내용을 json.loads()로 파싱
        response_data = json.loads(response.content)
        
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'question_id not provided')

    def test_delete_image_question_not_found(self):
        request = self.factory.post('/delete-image/', data={'question_id': 999})
        response = delete_image(request)

        self.assertEqual(response.status_code, 200)
        
        # 응답 내용을 json.loads()로 파싱
        response_data = json.loads(response.content)
        
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Question not found')

    def tearDown(self):
        # 테스트가 끝난 후 생성된 파일을 삭제합니다.
        if os.path.exists(self.image_path):
            os.remove(self.image_path)