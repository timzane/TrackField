# Generated by Django 4.0.6 on 2022-08-22 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_performance_performancenote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='athlete',
            name='created',
        ),
        migrations.RemoveField(
            model_name='athlete',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='event',
            name='created',
        ),
        migrations.RemoveField(
            model_name='event',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='meet',
            name='created',
        ),
        migrations.RemoveField(
            model_name='meet',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='created',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='updated',
        ),
    ]
