# Generated by Django 4.2.5 on 2023-09-29 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(db_index=True, max_length=50, verbose_name='customer')),
                ('plate', models.CharField(max_length=10, verbose_name='plate')),
                ('vin', models.CharField(max_length=17, verbose_name='vin')),
                ('color', models.CharField(max_length=20, verbose_name='color')),
            ],
            options={
                'verbose_name': 'car',
                'verbose_name_plural': 'cars',
                'ordering': ['customer'],
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(db_index=True, max_length=50, verbose_name='brand')),
                ('model', models.CharField(db_index=True, max_length=50, verbose_name='model')),
                ('year', models.IntegerField(db_index=True, verbose_name='year')),
            ],
            options={
                'verbose_name': 'carmodel',
                'verbose_name_plural': 'carmodels',
                'ordering': ['brand', 'model', 'year'],
            },
        ),
        migrations.CreateModel(
            name='PartService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='price')),
            ],
            options={
                'verbose_name': 'partservice',
                'verbose_name_plural': 'partservices',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'pending'), (1, 'in progress'), (2, 'completed'), (3, 'cancelled')], default=0, verbose_name='status')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='autoservisas.car', verbose_name='car')),
            ],
            options={
                'verbose_name': 'serviceorder',
                'verbose_name_plural': 'serviceorders',
                'ordering': ['car'],
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='autoservisas.serviceorder', verbose_name='order')),
                ('part_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='autoservisas.partservice', verbose_name='part service id')),
            ],
            options={
                'verbose_name': 'orderline',
                'verbose_name_plural': 'orderlines',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='car',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='autoservisas.carmodel', verbose_name='carmodel'),
        ),
    ]
