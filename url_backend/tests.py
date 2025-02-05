from django.test import TestCase, Client

class URLShortenerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_shorten_and_redirect(self):
        response = self.client.post('/shorten', data='{"long_url": "http://example.com"}', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        short_url = response.json()['short_url']
        short_code = short_url.split('/')[-1]

        response = self.client.get(f'/{short_code}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "http://example.com")

    def test_invalid_url(self):
        response = self.client.post('/shorten', data='{"long_url": "invalid_url"}', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_duplicate_url(self):
        self.client.post('/shorten', data='{"long_url": "http://example.com"}', content_type='application/json')
        response = self.client.post('/shorten', data='{"long_url": "http://example.com"}', content_type='application/json')
        self.assertEqual(response.status_code, 200)
