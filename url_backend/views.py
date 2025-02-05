from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import URLValidator
from rest_framework.throttling import AnonRateThrottle
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import URL


class URLShortenRateThrottle(AnonRateThrottle):
    rate = '10/min'


class ShortenURLAPIView(APIView):
    throttle_classes = [URLShortenRateThrottle]

    def post(self, request):
        long_url = request.data.get('long_url')

        if not long_url:
            return Response({'error': 'long_url is required'}, status=status.HTTP_400_BAD_REQUEST)

        validator = URLValidator()
        try:
            validator(long_url)
        except ValidationError:
            return Response({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)

        url_obj, created = URL.objects.get_or_create(long_url=long_url)
        if created:
            url_obj.short_code = get_random_string(6)
            url_obj.save()

        short_url = f"{settings.DOMAIN}/{url_obj.short_code}"
        return Response({'short_url': short_url}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class URLRedirectAPIView(APIView):
    def get(self, request, short_code):
        try:
            url_obj = URL.objects.get(short_code=short_code)
            return redirect(url_obj.long_url)
        except URL.DoesNotExist:
            return Response({'error': 'Short URL not found'}, status=status.HTTP_404_NOT_FOUND)

def home(request):
    return render(request, 'shortener/home.html')
