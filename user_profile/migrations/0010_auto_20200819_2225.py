# Generated by Django 3.1 on 2020-08-19 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0009_auto_20200819_2201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='cropping',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='profile_picture'),
        ),
    ]
