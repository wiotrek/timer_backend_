from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Score(models.Model):
    name = models.PositiveIntegerField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=settings.AUTH_USER_MODEL)

