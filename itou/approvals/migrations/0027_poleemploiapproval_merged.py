# Generated by Django 4.0.1 on 2022-02-07 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("approvals", "0026_auto_20220203_1620"),
    ]

    operations = [
        migrations.AddField(
            model_name="poleemploiapproval",
            name="merged",
            field=models.BooleanField(default=False, verbose_name="Agrément fusionné avec les doublons?"),
        ),
    ]
