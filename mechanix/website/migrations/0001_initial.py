# Generated by Django 3.2.9 on 2021-12-06 10:41

from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0023_auto_20211206_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_content', serialize=False, to='cms.cmsplugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentEntry',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contententry', serialize=False, to='cms.cmsplugin')),
                ('htmlID', models.CharField(max_length=128)),
                ('heading', models.CharField(max_length=256)),
                ('subheading', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentFlow',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contentflow', serialize=False, to='cms.cmsplugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentFlowEntryHTML',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contentflowentryhtml', serialize=False, to='cms.cmsplugin')),
                ('text', djangocms_text_ckeditor.fields.HTMLField()),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentFlowEntryImage',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contentflowentryimage', serialize=False, to='cms.cmsplugin')),
                ('image', models.ImageField(upload_to='Mechanix/Flow')),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=256, null=True)),
                ('content', models.CharField(blank=True, max_length=2048, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentGallery',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contentgallery', serialize=False, to='cms.cmsplugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentGalleryEntry',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contentgalleryentry', serialize=False, to='cms.cmsplugin')),
                ('image', models.ImageField(upload_to='Mechanix/Gallery')),
                ('alt', models.CharField(max_length=512)),
                ('url', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentGrid',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contentgrid', serialize=False, to='cms.cmsplugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentHighlights',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contenthighlights', serialize=False, to='cms.cmsplugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentHighlightsEntry',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contenthighlightsentry', serialize=False, to='cms.cmsplugin')),
                ('faIcon', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=2048)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentTeam',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contentteam', serialize=False, to='cms.cmsplugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ContentTeamEntry',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_contentteamentry', serialize=False, to='cms.cmsplugin')),
                ('squareImage', models.ImageField(blank=True, null=True, upload_to='Mechanix/Team/Square')),
                ('verticalImage', models.ImageField(blank=True, null=True, upload_to='Mechanix/Team/Vertical')),
                ('name', models.CharField(max_length=128)),
                ('function', models.CharField(blank=True, max_length=128, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=512, null=True)),
                ('mail', models.CharField(blank=True, max_length=512, null=True)),
                ('text', djangocms_text_ckeditor.fields.HTMLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_footer', serialize=False, to='cms.cmsplugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='FooterFontAwesomeEntry',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_footerfontawesomeentry', serialize=False, to='cms.cmsplugin')),
                ('faClass', models.CharField(max_length=512)),
                ('url', models.CharField(max_length=512)),
                ('pos', models.CharField(choices=[('L', 'Left'), ('M', 'Middle'), ('R', 'Right')], max_length=16)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='FooterHTMLEntry',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_footerhtmlentry', serialize=False, to='cms.cmsplugin')),
                ('text', djangocms_text_ckeditor.fields.HTMLField()),
                ('pos', models.CharField(choices=[('L', 'Left'), ('M', 'Middle'), ('R', 'Right')], max_length=16)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='FooterTextEntry',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_footertextentry', serialize=False, to='cms.cmsplugin')),
                ('text', models.CharField(max_length=512)),
                ('url', models.CharField(blank=True, max_length=512, null=True)),
                ('pos', models.CharField(choices=[('L', 'Left'), ('M', 'Middle'), ('R', 'Right')], max_length=16)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Masthead',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_masthead', serialize=False, to='cms.cmsplugin')),
                ('subText', models.CharField(blank=True, max_length=256, null=True)),
                ('headText', models.CharField(blank=True, max_length=256, null=True)),
                ('buttonLink', models.CharField(blank=True, max_length=512, null=True)),
                ('buttonText', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
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
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='website_menuitem', serialize=False, to='cms.cmsplugin')),
                ('displayName', models.CharField(max_length=128)),
                ('pageID', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
