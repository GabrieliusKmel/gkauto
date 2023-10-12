# Generated by Django 4.2.5 on 2023-10-10 08:25

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0008_alter_partservice_problem_carpartservice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partservice',
            name='problem',
        ),
        migrations.AddField(
            model_name='carpartservice',
            name='problem',
            field=tinymce.models.HTMLField(blank=True, default='', max_length=10000, verbose_name='problem'),
        ),
    ]