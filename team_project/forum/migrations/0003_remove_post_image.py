# Generated by Django 4.1.7 on 2023-04-13 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]