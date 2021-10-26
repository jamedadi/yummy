from django.db import models
from django.utils.text import slugify

from accounts.models import ServiceProvider
from library.models import BaseModel
from django.utils.translation import ugettext_lazy as _
from address.models import ServiceAddress, Area
import uuid


class Service(BaseModel):
    RESTAURANT = 0
    CAFE = 1
    CONFECTIONERY = 2
    SUPERMARKET = 3

    SERVICE_TYPES = (
        (RESTAURANT, _('restaurant')),
        (CAFE, _('cafe')),
        (CONFECTIONERY, _('confectionery')),
        (SUPERMARKET, _('supermarket')),
    )

    uuid = models.UUIDField(default=uuid.uuid4, verbose_name=_('uuid'), unique=True, db_index=True)
    service_provider = models.ForeignKey(
        ServiceProvider,
        verbose_name=_('service provider'),
        related_name='services',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=40, verbose_name=_('name'))
    service_type = models.PositiveSmallIntegerField(verbose_name=_('service type'), choices=SERVICE_TYPES)
    minimum_purchase = models.DecimalField(max_digits=9, decimal_places=0, verbose_name=_('minimum purchase'))
    available = models.BooleanField(default=False, verbose_name=_('available'))
    logo = models.ImageField(verbose_name=_('logo'), upload_to='service/logos/', null=True, blank=True)
    banner = models.ImageField(verbose_name=_('banner'), upload_to='service/banners/', null=True, blank=True)

    address = models.OneToOneField(
        ServiceAddress,
        verbose_name=_('address'),
        related_name='services',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.name} - {self.get_service_type_display()}'

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        db_table = 'service'
        ordering = ('created_time',)


class ServiceCategory(BaseModel):
    name = models.CharField(max_length=30, verbose_name=_('name'))
    slug = models.SlugField(max_length=35, verbose_name=_('slug'), allow_unicode=True)
    service = models.ForeignKey(Service, verbose_name=_('service'), related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.service.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('ServiceCategory')
        verbose_name_plural = _('ServiceCategories')
        db_table = 'service_category'


class DeliveryArea(BaseModel):
    service = models.ForeignKey(
        Service, verbose_name=_('service'), related_name='delivery_areas', on_delete=models.CASCADE
    )
    area = models.ForeignKey(Area, verbose_name=_('area'), related_name='delivery_areas', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.service.name} - {self.area}'

    class Meta:
        verbose_name = _('DeliveryArea')
        verbose_name_plural = _('DeliveryAreas')
        db_table = 'delivery_area'


class ServiceAvailableTime(BaseModel):
    SAT_DAY = 0
    SUN_DAY = 1
    MON_DAY = 2
    TUE_DAY = 3
    WED_DAY = 4
    THU_DAY = 5
    FRI_DAY = 6

    DAYS = (
        (SAT_DAY, _('saturday')),
        (SUN_DAY, _('sunday')),
        (MON_DAY, _('monday')),
        (TUE_DAY, _('tuesday')),
        (WED_DAY, _('wednesday')),
        (THU_DAY, _('thursday')),
        (FRI_DAY, _('friday'))
    )
    service = models.ForeignKey(
        Service, verbose_name=_('service'), related_name='available_times', on_delete=models.CASCADE
    )
    day = models.PositiveSmallIntegerField(verbose_name=_('day'), choices=DAYS, null=True)
    open_time = models.TimeField(verbose_name=_('open time'), null=True)
    close_time = models.TimeField(verbose_name=_('close time'), null=True)
    is_close = models.BooleanField(verbose_name=_('close day'), blank=True, null=True)

    def __str__(self):
        return f'{self.service.name} - {self.get_day_display()} - ' \
               f'{self.is_close if self.close_time else self.open_time and "-" and self.close_time}'

    class Meta:
        verbose_name = _('ServiceAvailableTime')
        verbose_name_plural = _('ServiceAvailableTimes')
        db_table = 'service_available_time'
        ordering = ('day',)
