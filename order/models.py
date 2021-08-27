from django.db import models
from library.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class Order(BaseModel):
    # TODO-1: add foreign key to invoice here
    # TODO-2: add status here
    is_delivered = models.BooleanField(verbose_name=_('is delivered'), default=False)
