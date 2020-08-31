# Generated by Django 3.1 on 2020-08-24 00:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_functionalities', '0018_auto_20200823_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='rating',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10, message="The rating can't be higher than 10")]),
        ),
    ]