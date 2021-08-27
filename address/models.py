from django.db import models
from library.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class State(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('name'))
    slug = models.SlugField(max_length=25, verbose_name=_('slug'), allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        db_table = 'state'


class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('name'))
    slug = models.SlugField(max_length=25, verbose_name=_('slug'), allow_unicode=True)
    state = models.ForeignKey(State, verbose_name=_('state'), related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.state} - {self.name}'

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        db_table = 'city'


class Area(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('name'))
    slug = models.SlugField(max_length=25, verbose_name=_('slug'), allow_unicode=True)
    city = models.ForeignKey(City, verbose_name=_('city'), related_name='areas', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city.name} - {self.name})'

    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')
        db_table = 'area'


class Address(BaseModel):
    state = models.ForeignKey(State, verbose_name=_('state'), related_name='addresses', on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name=_('city'), related_name='addresses', on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name=_('area'), related_name='addresses', on_delete=models.CASCADE)
    floor = models.SmallIntegerField(verbose_name=_('floor'))
    plaque = models.SmallIntegerField(verbose_name=_('plaque'))

    def __str__(self):
        return f'{self.area} - {self.floor} - {self.plaque}'

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        db_table = 'address'
