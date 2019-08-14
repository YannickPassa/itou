# Generated by Django 2.2.4 on 2019-08-14 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
        ('siae', '0002_auto_20190807_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='siae',
            name='brand',
            field=models.CharField(blank=True, max_length=256, verbose_name='Enseigne'),
        ),
        migrations.AddField(
            model_name='siae',
            name='job_appellations',
            field=models.ManyToManyField(blank=True, to='jobs.Appellation', verbose_name='Métiers'),
        ),
        migrations.AddField(
            model_name='siae',
            name='website',
            field=models.URLField(blank=True, verbose_name='Site web'),
        ),
    ]
