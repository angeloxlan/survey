from django.db import models
from .survey import Survey


class Submission(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE
    )
    submited_at = models.DateTimeField(auto_now_add=True)
