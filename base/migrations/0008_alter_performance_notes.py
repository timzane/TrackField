# Generated by Django 4.0.6 on 2022-08-26 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_performance_archive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='Notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
