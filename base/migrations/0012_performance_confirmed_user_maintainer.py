# Generated by Django 4.0.6 on 2022-09-01 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_user_editor'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='Confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Maintainer',
            field=models.BooleanField(default=False),
        ),
    ]
