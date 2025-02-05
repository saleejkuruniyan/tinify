from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import URL

class URLShortenerAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.long_url = "https://www.example.com"
        self.shorten_url_endpoint = reverse('shorten_url')  # Assuming you've named the URL pattern

    def test_shorten_valid_url(self):
        response = self.client.post(self.shorten_url_endpoint, {"long_url": self.long_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('short_url', response.data)

    def test_shorten_invalid_url(self):
        response = self.client.post(self.shorten_url_endpoint, {"long_url": "invalid-url"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_shorten_missing_url(self):
        response = self.client.post(self.shorten_url_endpoint, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_redirect_valid_short_code(self):
        url_obj = URL.objects.create(long_url=self.long_url, short_code="abc123")
        response = self.client.get(f"/{url_obj.short_code}/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, self.long_url)

    def test_redirect_invalid_short_code(self):
        response = self.client.get("/nonexistent/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)


class RateLimitingTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.shorten_url = reverse('shorten_url')
        self.long_url = "https://www.example.com"

    def test_rate_limiting(self):
        # Send 10 successful requests
        for _ in range(10):
            response = self.client.post(self.shorten_url, {"long_url": self.long_url}, format='json')
            self.assertNotEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        # 11th request should be rate-limited
        response = self.client.post(self.shorten_url, {"long_url": self.long_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Request was throttled. Expected available in 60 seconds.')
