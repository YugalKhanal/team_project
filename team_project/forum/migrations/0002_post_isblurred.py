# Generated by Django 4.1.7 on 2023-04-16 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='isBlurred',
            field=models.BooleanField(default=False),
        ),
    ]