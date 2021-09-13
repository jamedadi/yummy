from django.db import models
from django.utils.translation import gettext as _

from gateway.utils.zarrinpal import zarrinpal_request_handler, zarrinpal_payment_verify
from library.models import BaseModel


class Gateway(BaseModel):
    FUNCTION_ZARRINPAL = 'zarrinpal'
    FUNCTION_SAMAN = 'saman'
    GATEWAY_FUNCTIONS_CHOICES = (
        (FUNCTION_ZARRINPAL, _('Zarrinpal')),
        (FUNCTION_SAMAN, _('Saman'))
    )

    title = models.CharField(max_length=100, verbose_name=_('title'))
    gateway_request_url = models.CharField(max_length=150, verbose_name=_('request url'), blank=True)
    gateway_verify_url = models.CharField(max_length=150, verbose_name=_('verify url'), blank=True)
    gateway_code = models.CharField(max_length=20, verbose_name=_('gateway code'), choices=GATEWAY_FUNCTIONS_CHOICES)
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    auth_data = models.TextField(verbose_name=_('auth data'), blank=True)

    def __str__(self):
        return self.title

    def get_request_handler(self):
        handlers = {
            self.FUNCTION_ZARRINPAL: zarrinpal_request_handler,
            self.FUNCTION_SAMAN: None,
        }
        return handlers[self.gateway_code]

    def get_verify_handler(self):
        handlers = {
            self.FUNCTION_ZARRINPAL: zarrinpal_payment_verify,
            self.FUNCTION_SAMAN: None,
        }
        return handlers[self.gateway_code]

    class Meta:
        verbose_name = _('Gateway')
        verbose_name_plural = _('Gateways')
        db_table = 'gateway'
