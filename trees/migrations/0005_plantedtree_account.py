# Generated by Django 5.0.2 on 2024-02-23 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trees", "0004_remove_plantedtree_age"),
    ]

    operations = [
        migrations.AddField(
            model_name="plantedtree",
            name="account",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="trees.account",
            ),
            preserve_default=False,
        ),
    ]
