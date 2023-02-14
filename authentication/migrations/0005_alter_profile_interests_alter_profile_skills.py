# Generated by Django 4.1.6 on 2023-02-09 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_post'),
        ('authentication', '0004_alter_profile_interests_alter_profile_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interests',
            field=models.ManyToManyField(blank=True, to='app.interest'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(blank=True, to='app.skill'),
        ),
    ]