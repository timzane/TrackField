# Generated by Django 4.0.6 on 2022-08-30 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_remove_performance_markraw'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Editor',
            field=models.BooleanField(default=False),
        ),
    ]
