from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils.text import slugify


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

    def save(self, *args, **kwargs):
        if not len(self.slug.strip()):
            self.slug = slugify(self.title)

        _slug = self.slug
        _count = 1

        while True:
            try:
                Survey.objects.all().exclude(pk=self.pk).get(slug=_slug)
            except MultipleObjectsReturned:
                pass
            except ObjectDoesNotExist:
                break
            _slug = "%s-%s" % (self.slug, _count)
            _count += 1

        self.slug = _slug

        super(Survey, self).save(*args, **kwargs)