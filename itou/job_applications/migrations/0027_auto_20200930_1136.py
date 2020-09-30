# Generated by Django 3.1.1 on 2020-09-30 09:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("job_applications", "0026_auto_20200803_1543"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplication",
            name="approval_number_refused_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Date de refus manuel du PASS IAE"),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="approval_number_refused_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="approval_numbers_refused",
                to=settings.AUTH_USER_MODEL,
                verbose_name="PASS IAE refusé manuellement par",
            ),
        ),
        migrations.AlterField(
            model_name="jobapplication",
            name="approval_number_delivered_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="approval_numbers_delivered",
                to=settings.AUTH_USER_MODEL,
                verbose_name="PASS IAE délivré manuellement par",
            ),
        ),
    ]
