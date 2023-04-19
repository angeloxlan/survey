from django.db import models
from .question import Question


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
