from django.test import TestCase
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_strawberry.settings")
django.setup()
from django.urls import reverse
from rest_framework.test import APIClient

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_index_loads_properly(self):
        response = self.client.get(reverse('start_page'))
        response = self.client.get(reverse('homepage'))
        response = self.client.get(reverse('login'))
        response = self.client.get(reverse('register'))
        response = self.client.get(reverse('login'))
        response = self.client.get(reverse('logout'))
        response = self.client.get(reverse('profile'))
        response = self.client.get(reverse('culture_list'))
        response = self.client.get(reverse('month_list'))
        response = self.client.get(reverse('calendar'))
        response = self.client.get(reverse('all_objects'))
        response = self.client.get(reverse('month_detail', kwargs={'year': 2023, 'month': 6}))
        response = self.client.get(reverse('upload_images'))
        response = self.client.get(reverse('delete_file', kwargs={'filename': 'IMG_20221011_141753.jpg'}))
        self.assertRedirects(response, reverse('upload_images'))
        response = self.client.get(reverse('upload_images'))

        response = self.client.get(reverse('choose_month'), follow=True)
        response = self.client.get(reverse('choose_month_with_id', kwargs={'month_id': 1}))

        response = self.client.get(reverse('choose_culture'))
        response = self.client.get(reverse('api_choose_culture_with_id', kwargs={'culture_id': 1}))
        response = self.client.get(reverse('api_choose_culture', kwargs={'culture_id': 1}))
        self.assertEqual(response.status_code, 200)


