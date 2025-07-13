from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    LANGUAGE_CHOICES = [
        ('ru', 'Russian'),
        ('en', 'English'),
    ]
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ru')
    theme = models.CharField(max_length=5, choices=THEME_CHOICES, default='light')
