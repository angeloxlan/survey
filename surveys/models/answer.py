from django.db import models
from .option import Option
from .submission import Submission


class Answer(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE
    )
    option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
