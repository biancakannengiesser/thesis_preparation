# Generated by Django 4.2 on 2023-05-21 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_userprofile_cv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cv',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
