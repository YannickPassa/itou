# Generated by Django 2.2.9 on 2020-02-10 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("siaes", "0016_auto_20200109_1010")]

    operations = [
        migrations.AddField(
            model_name="siae",
            name="auth_email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="E-mail d'authentification"
            ),
        )
    ]
