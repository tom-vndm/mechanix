# Generated by Django 3.2.9 on 2021-12-07 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fobi', '0016_auto_20211206_1039'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='forms',
            field=models.ManyToManyField(to='fobi.FormEntry'),
        ),
    ]