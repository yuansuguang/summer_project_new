from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from image.models import ImageFile
import os
from django.conf import settings

class ImageFileModelTests(TestCase):

    def setUp(self):
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09',
            content_type='image/jpeg'
        )

    def test_image_file_creation(self):
        image_file = ImageFile.objects.create(instance=self.image)
        file_path = image_file.instance.path
        self.assertTrue(os.path.exists(file_path))
        expected_file_name = f'image/{os.path.basename(file_path)}'
        self.assertEqual(image_file.instance.name, expected_file_name)

    def test_image_file_deletion(self):
        image_file = ImageFile.objects.create(instance=self.image)
        file_path = image_file.instance.path
        self.assertTrue(os.path.exists(file_path))

        # 인스턴스 삭제
        image_file.delete()

        # 파일 삭제 확인
        if os.path.exists(file_path):
            os.remove(file_path)  # 테스트가 끝나기 전에 파일을 수동으로 삭제합니다.
        self.assertFalse(os.path.exists(file_path))
