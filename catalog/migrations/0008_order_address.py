# Generated by Django 4.0.2 on 2022-03-04 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_orderdetail_flashlight_orderdetail_helmet_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default=1, help_text='format: required', max_length=255, verbose_name='адрес доставки'),
            preserve_default=False,
        ),
    ]