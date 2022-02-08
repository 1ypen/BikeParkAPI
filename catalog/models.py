from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from datetime import datetime
import pytz

User = get_user_model()


class Brand(models.Model):
    name = models.CharField(
        max_length=255
    )


class Media(models.Model):
    image = models.ImageField(upload_to='media/bicycle/')


class Bicycle(models.Model):

    class BicycleType(models.TextChoices):
        CITY = 'CT', _('Городской')
        SPORT = 'SP', _('Спортивный')
        MOUNTAIN = 'MN', _('Горный')

    class Material(models.TextChoices):
        ALUMINUM = 'AL', _('Алюминий')
        CARBON = 'CR', _('Карбон')
        STEEL = 'ST', _('Метал')

    class Size(models.TextChoices):
        XS = 'XS', _('XS')
        S = 'S', _('S')
        M = 'M', _('M')
        L = 'L', _('L')
        XL = 'XL', _('XL')
        XXL = 'XXL', _('XXL')

    name = models.CharField(
        max_length=255,
        verbose_name=_('Название'),
        help_text=_(
            'format: required, char, max-255'
        )
    )
    cover_image = models.ImageField(
        upload_to='media/bicycle/'
    )
    images = models.ManyToManyField(
        Media
    )

    weight_in_kg = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=_('Вес(кг)'),
        help_text=_(
            'format: required, decimal, max_length-4, decimal_places-2'
        )
    )
    number_of_speeds = models.IntegerField(
        verbose_name=_('Количество скоростей'),
        help_text=_(
            'format: required'
        )
    )

    depreciation = models.BooleanField(
        verbose_name=_('Aмортизация'),
        help_text=_(
            'format: required, true=there is depreciation'
        )
    )

    type = models.CharField(
        max_length=2,
        choices=BicycleType.choices,
        verbose_name=_('Тип велосипеда')
    )

    material = models.CharField(
        max_length=2,
        choices=Material.choices,
        verbose_name=_('Материал рамы')
    )

    size = models.CharField(
        max_length=3,
        choices=Size.choices,
        verbose_name=_('Размеры рамы')
    )

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)

    wheel_diameter = models.IntegerField(
        verbose_name=_('диаметр колес'),
        help_text=_(
            'format: required'
        )
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Доступен?'),
        help_text=_("format: true=bicycle visible")
    )

    def __str__(self):
        return self.name


class Price(models.Model):
    bicycle = models.ForeignKey(
        Bicycle,
        on_delete=models.DO_NOTHING,
        verbose_name=_('велосипед'),
        help_text=_('format: required, bicycle foreignkey'),
        related_name='prices'
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=7,
        verbose_name=_('цена велосипеда'),
        help_text=_('format: required, decimal_places=2, max_digits=7')
    )
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('дата создания цены'),
        help_text=_('format: required')
    )
    end_date = models.DateTimeField(
        default=datetime(
            year=2999,
            month=12,
            day=31,
            hour=12,
            tzinfo=pytz.UTC
        ),
        verbose_name=_('дата окончания цены'),
        help_text=_('format: required')
    )
    is_current = models.BooleanField(
        default=True,
        verbose_name=_('актуальность цены'),
        help_text=_('format: required, true=current')
    )


class Order(models.Model):
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания записи')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Aрендатор'),
        related_name='orders'
    )
    total_sum = models.IntegerField()


class OrderDetail(models.Model):

    start_date = models.DateTimeField(
        verbose_name=_('Дата начала аренды')
    )
    end_date = models.DateTimeField(
        verbose_name=_('Дата конца аренды')
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        related_name='order_details'
    )

    bicycle_price = models.DecimalField(
        decimal_places=2,
        max_digits=7,
        verbose_name=_('цена велосипеда'),
        help_text=_('format: required, decimal_places=2, max_digits=7')
    )

    bicycle = models.ForeignKey(
        Bicycle,
        on_delete=models.DO_NOTHING,
        related_name='order_details'
    )
