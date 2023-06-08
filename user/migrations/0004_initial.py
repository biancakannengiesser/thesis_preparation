# Generated by Django 4.2 on 2023-05-08 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_delete_teammember'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMemberRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('phone_number', models.CharField(max_length=10, verbose_name='Contact Phone')),
                ('email_address', models.EmailField(max_length=254)),
                ('motivation', models.TextField(max_length=250, verbose_name='Motivation')),
                ('resume', models.FileField(upload_to='')),
            ],
        ),
    ]
