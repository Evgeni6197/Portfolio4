# Generated by Django 4.1.1 on 2023-05-22 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0005_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="datetime_editing",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
