from django.test import TestCase

# Create your tests here.
from .models import Video

class VideoModelTestCase(TestCase):
    def setUp(self):
        Video.objects.create(title="This is my test video")

    def test_valid_title(self):
        title="This is my test video"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())