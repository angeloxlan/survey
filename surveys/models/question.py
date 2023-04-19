from django.db import models
from .survey import Survey


class Question(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
