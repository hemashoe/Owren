# Generated by Django 4.1.6 on 2023-02-08 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_interest_name_alter_interest_slug_and_more'),
        ('authentication', '0003_profile_interests_profile_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interests',
            field=models.ManyToManyField(blank=True, null=True, to='app.interest'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(blank=True, null=True, to='app.skill'),
        ),
    ]
