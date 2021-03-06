# Generated by Django 3.2.9 on 2021-12-07 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_forms'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='externalButtonText',
            field=models.CharField(default='def', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='externalButtonUrl',
            field=models.CharField(default='def', max_length=512),
            preserve_default=False,
        ),
    ]
