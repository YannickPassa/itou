# Generated by Django 3.2.8 on 2021-11-04 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("siaes", "0050_alter_siae_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="siae",
            name="historization_admin",
            field=models.TextField(blank=True, verbose_name="Commentaires des admins"),
        ),
        migrations.AddField(
            model_name="siaeconvention",
            name="historization_admin",
            field=models.TextField(blank=True, verbose_name="Commentaires des admins"),
        ),
    ]
