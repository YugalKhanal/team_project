# Generated by Django 4.1.7 on 2023-04-15 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('venue', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('image', models.ImageField(upload_to='')),
                ('thumbnail', models.ImageField(upload_to='')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.category')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_by_users', to='events.events')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'event')},
            },
        ),
    ]
