from django.db import models

class URL(models.Model):
    long_url = models.URLField(unique=True)
    short_code = models.CharField(max_length=10, unique=True)
