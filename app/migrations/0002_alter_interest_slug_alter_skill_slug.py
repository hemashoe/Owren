# Generated by Django 4.1.7 on 2023-03-11 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
