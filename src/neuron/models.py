from django.db import models

class APIKey(models.Model):
    api_key = models.CharField(max_length=32)
    api_secret_key = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)

    