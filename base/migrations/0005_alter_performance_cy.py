# Generated by Django 4.0.6 on 2022-08-24 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_athlete_created_athlete_updated_event_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='CY',
            field=models.IntegerField(null=True),
        ),
    ]
