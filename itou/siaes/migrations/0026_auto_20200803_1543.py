# Generated by Django 3.0.7 on 2020-08-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("siaes", "0025_auto_20200723_1447")]

    operations = [
        migrations.AlterField(
            model_name="siae",
            name="active_until",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Date de désactivation"),
        )
    ]
