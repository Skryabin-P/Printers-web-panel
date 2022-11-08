# Generated by Django 3.2.14 on 2022-11-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_givedrum'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObmenFolders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя папки')),
                ('description', models.TextField(verbose_name='Описание')),
                ('visible', models.BooleanField(verbose_name='Показывать папку')),
            ],
        ),
    ]