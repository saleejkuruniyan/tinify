from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from .models import URL
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt


class ShortenURLView(View):
    @method_decorator(csrf_exempt)

    def post(self, request):
        import json
        data = json.loads(request.body)
        long_url = data.get('long_url')

        validator = URLValidator()
        try:
            validator(long_url)
        except ValidationError:
            return HttpResponseBadRequest("Invalid URL")

        url_obj, created = URL.objects.get_or_create(long_url=long_url)
        if created:
            url_obj.short_code = get_random_string(6)
            url_obj.save()

        return JsonResponse({'short_url': f"http://tinify.needoo.in/{url_obj.short_code}"})

class RedirectURLView(View):
    @method_decorator(csrf_exempt)

    def get(self, request, short_code):
        url_obj = get_object_or_404(URL, short_code=short_code)
        return redirect(url_obj.long_url)
