# Generated by Django 4.1.7 on 2023-03-13 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_events_venue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="events",
            name="slug",
            field=models.SlugField(editable=False, unique=True),
        ),
    ]