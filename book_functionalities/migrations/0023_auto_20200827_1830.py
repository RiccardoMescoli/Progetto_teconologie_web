# Generated by Django 3.1 on 2020-08-27 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_functionalities', '0022_auto_20200827_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewreport',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='book_functionalities.bookreview'),
        ),
    ]
