# Generated by Django 4.1.6 on 2023-02-10 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]