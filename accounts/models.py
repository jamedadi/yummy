from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    #  this model is used for admins and superusers
    # TODO : AUTH_USER_MODEL must be changed to this model in settings

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'


class CustomerManager(UserManager):
    def _create_user(self, phone_number, password, **extra_fields):

        if not phone_number:
            raise ValueError('The given phone must be set')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=13, verbose_name=_('phone number'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomerManager()

    @property
    def full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        db_table = 'customer'


class ServiceProvider(AbstractUser):
    email = models.EmailField(_('email address'), blank=True, unique=True)
    phone_number = models.CharField(max_length=13, verbose_name=_('phone number'), unique=True)

    class Meta:
        verbose_name = _('service provider')
        verbose_name_plural = _('service providers')
        db_table = 'service_provider'
