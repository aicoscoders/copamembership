# Generated by Django 4.1.3 on 2022-11-25 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0002_group_users"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group", name="description", field=models.TextField(null=True),
        ),
    ]
