# Generated by Django 3.2.9 on 2022-06-17 18:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_img', verbose_name='image')),
                ('ph_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('join_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='join_date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]