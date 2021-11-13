# Generated by Django 3.2.9 on 2021-11-13 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0023_auto_20211105_1037'),
        ('website', '0010_alter_contentteamentry_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='MastheadImage',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_mastheadimage', serialize=False, to='cms.cmsplugin')),
                ('image', models.ImageField(upload_to='Mechanix/Masthead')),
                ('headCaption', models.CharField(max_length=256)),
                ('subCaption', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.RemoveField(
            model_name='mastheadcontent',
            name='cmsplugin_ptr',
        ),
        migrations.RemoveField(
            model_name='masthead',
            name='alt',
        ),
        migrations.RemoveField(
            model_name='masthead',
            name='background',
        ),
        migrations.AddField(
            model_name='masthead',
            name='buttonLink',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='masthead',
            name='buttonText',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='masthead',
            name='headText',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='masthead',
            name='subText',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.DeleteModel(
            name='MastheadButton',
        ),
        migrations.DeleteModel(
            name='MastheadContent',
        ),
    ]