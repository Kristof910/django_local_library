# Generated by Django 4.1.5 on 2023-02-02 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="language",
            field=models.CharField(default="", max_length=30),
        ),
    ]
