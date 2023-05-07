from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
