# Generated by Django 4.2.5 on 2023-10-06 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autoservisas', '0005_partservice_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartServiceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=4000, verbose_name='Content')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('partservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='autoservisas.partservice', verbose_name='partservice')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partservice_reviews', to=settings.AUTH_USER_MODEL, verbose_name='reviewer')),
            ],
            options={
                'verbose_name': 'partservice review',
                'verbose_name_plural': 'partservice reviews',
                'ordering': ['-created_at'],
            },
        ),
    ]
