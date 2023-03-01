# Generated by Django 3.2.14 on 2023-02-15 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Отдел')),
            ],
        ),
        migrations.CreateModel(
            name='DrumList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Драм')),
            ],
        ),
        migrations.CreateModel(
            name='PlacesList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Площадка')),
            ],
        ),
        migrations.CreateModel(
            name='PrinterModelList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Модель принтера')),
            ],
        ),
        migrations.CreateModel(
            name='TonerModelList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Модель картриджа')),
            ],
        ),
        migrations.CreateModel(
            name='PrintersMain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(protocol='IPv4', unique=True, verbose_name='IP')),
                ('comment', models.CharField(max_length=200, verbose_name='Комментарий')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_dashboard.placeslist', verbose_name='Площадка')),
                ('printermodel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_dashboard.printermodellist', verbose_name='Модель принтера')),
                ('toner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_dashboard.tonermodellist', verbose_name='Модель картриджа')),
            ],
        ),
    ]
