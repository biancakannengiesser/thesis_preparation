# Generated by Django 4.2 on 2023-06-12 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_lesson_quiz_quizoption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
    ]