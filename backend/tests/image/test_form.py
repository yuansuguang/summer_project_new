from django.test import TestCase
from image.form import upload_image_form
from django.core.files.uploadedfile import SimpleUploadedFile

class ImageFormTest(TestCase):

    def test_upload_image_form_valid(self):
        image_data = SimpleUploadedFile(
            "test_image.jpg", 
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x0A\x00\x01\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B', 
            content_type="image/jpeg"
        )
        form = upload_image_form(data={}, files={'image': image_data})
        self.assertTrue(form.is_valid())

    def test_upload_image_form_invalid(self):
        form = upload_image_form(data={}, files={})
        self.assertFalse(form.is_valid())

    def test_upload_image_form_invalid_file_type(self):
        invalid_file = SimpleUploadedFile("test_file.txt", b"file_content", content_type="text/plain")
        form = upload_image_form(data={}, files={'image': invalid_file})
        self.assertFalse(form.is_valid())


#해결
