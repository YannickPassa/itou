# Generated by Django 3.0.4 on 2020-05-06 13:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("prescribers", "0016_auto_20200505_1544"),
    ]

    operations = [
        migrations.RemoveField(model_name="prescriberorganization", name="authorization_refused_at"),
        migrations.RemoveField(model_name="prescriberorganization", name="authorization_refused_by"),
        migrations.RemoveField(model_name="prescriberorganization", name="authorization_validated_at"),
        migrations.RemoveField(model_name="prescriberorganization", name="authorization_validated_by"),
        migrations.RemoveField(model_name="prescriberorganization", name="authorization_validation_required"),
        migrations.AddField(
            model_name="prescriberorganization",
            name="authorization_status",
            field=models.CharField(
                choices=[
                    ("NOT_SET", "Habilitation en attente de validation"),
                    ("VALIDATED", "Habilitation validée"),
                    ("REFUSED", "Validation de l'habilitation refusée"),
                ],
                default="NOT_SET",
                max_length=20,
                verbose_name="Statut de l'habilitation",
            ),
        ),
        migrations.AddField(
            model_name="prescriberorganization",
            name="authorization_updated_at",
            field=models.DateTimeField(null=True, verbose_name="Date de MAJ du statut de l'habilitation"),
        ),
        migrations.AddField(
            model_name="prescriberorganization",
            name="authorization_updated_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="authorization_status_set",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Dernière MAJ de l'habilitation par",
            ),
        ),
    ]
