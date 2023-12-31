# Generated by Django 4.2.5 on 2023-10-04 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0002_alter_orderline_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='carmodel_covers', verbose_name='cover'),
        ),
        migrations.AlterField(
            model_name='orderline',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=18, verbose_name='price'),
        ),
    ]
