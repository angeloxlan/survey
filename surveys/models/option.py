from django.db import models
from .question import Question
from .submission import Submission


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    def rate(self):
        total_submissions = Submission.objects.filter(
            survey__question__option=self).count()
        option_submissions = Submission.objects.filter(
            survey__question__option=self, answer__option=self).count()
        
        if total_submissions > 0:
            return (option_submissions / total_submissions) * 100
        else:
            return 0
