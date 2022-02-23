# Generated by Django 4.0.2 on 2022-02-23 11:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bicycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, max_len-255', max_length=255, verbose_name='Название')),
                ('cover_image', models.ImageField(upload_to='bicycle/', verbose_name='главная фотография велосипеда')),
                ('weight_in_kg', models.DecimalField(decimal_places=2, help_text='format: required, decimal, max_length-4, decimal_places-2', max_digits=4, verbose_name='Вес(кг)')),
                ('number_of_speeds', models.IntegerField(help_text='format: required', verbose_name='Количество скоростей')),
                ('depreciation', models.BooleanField(help_text='format: required, true=there is depreciation', verbose_name='Aмортизация')),
                ('type', models.CharField(choices=[('CT', 'Городской'), ('SP', 'Спортивный'), ('MN', 'Горный')], max_length=2, verbose_name='Тип велосипеда')),
                ('material', models.CharField(choices=[('AL', 'Алюминий'), ('CR', 'Карбон'), ('ST', 'Метал')], max_length=2, verbose_name='Материал рамы')),
                ('size', models.CharField(choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], max_length=3, verbose_name='Размеры рамы')),
                ('wheel_diameter', models.IntegerField(help_text='format: required', verbose_name='диаметр колес')),
                ('is_active', models.BooleanField(default=True, help_text='format: true=bicycle visible', verbose_name='Доступен?')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='format: required, max_len-255', max_length=255, verbose_name='имя бренда')),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='bicycle/')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('total_sum', models.DecimalField(decimal_places=2, help_text='format: required, decimal_places=2, max_digits=10', max_digits=10, verbose_name='полная сумма заказа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Aрендатор')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, help_text='format: required, decimal_places=2, max_digits=7', max_digits=7, verbose_name='цена велосипеда')),
                ('start_date', models.DateTimeField(auto_now_add=True, help_text='format: required', verbose_name='дата создания цены')),
                ('end_date', models.DateTimeField(default=datetime.datetime(2999, 12, 31, 12, 0, tzinfo=utc), help_text='format: required', verbose_name='дата окончания цены')),
                ('is_current', models.BooleanField(default=True, help_text='format: required, true=current', verbose_name='актуальность цены')),
                ('bicycle', models.ForeignKey(help_text='format: required, bicycle foreignkey', on_delete=django.db.models.deletion.DO_NOTHING, related_name='prices', to='catalog.bicycle', verbose_name='велосипед')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(help_text='format: YYYY-MM-DD H:M', verbose_name='Дата начала аренды')),
                ('end_date', models.DateTimeField(help_text='format: YYYY-MM-DD H:M', verbose_name='Дата конца аренды')),
                ('bicycle_price', models.DecimalField(decimal_places=2, help_text='format: required, decimal_places=2, max_digits=7', max_digits=7, verbose_name='цена велосипеда')),
                ('bicycle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_details', to='catalog.bicycle')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_details', to='catalog.order')),
            ],
        ),
        migrations.AddField(
            model_name='bicycle',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.brand'),
        ),
        migrations.AddField(
            model_name='bicycle',
            name='images',
            field=models.ManyToManyField(to='catalog.Media', verbose_name='фотографии велосипеда'),
        ),
    ]
