from django.test import SimpleTestCase
from django.urls import reverse, resolve
from image.views import upload_image

class TestUrls(SimpleTestCase):

    def test_upload_image_url_is_resolved(self):
        url = reverse('upload_image')
        self.assertEqual(resolve(url).func, upload_image)
