# Generated by Django 3.1 on 2020-09-17 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_auto_20200908_1032"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_stats_vip",
            field=models.BooleanField(default=False, verbose_name="Pilotage"),
        ),
    ]
