# Generated by Django 3.1 on 2020-08-22 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_functionalities', '0011_bookreview_spoiler'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='content',
            field=models.CharField(max_length=500),
        ),
    ]
