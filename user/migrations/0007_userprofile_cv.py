# Generated by Django 4.2 on 2023-05-21 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_userprofile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cv',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
