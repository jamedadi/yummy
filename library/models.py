from django.db import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(verbose_name='created time', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='modified time', auto_now=True)

    class Meta:
        abstract = True
