# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-15 19:02
from __future__ import unicode_literals

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
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('profile', models.CharField(choices=[('ADMINISTRATOR', 'ADMINISTRATOR'), ('MANAGER', 'MANAGER'), ('OPERATOR', 'OPERATOR'), ('USER', 'USER')], max_length=20, verbose_name='profile')),
                ('is_active', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('list_user', 'Can list existing users'),),
            },
        ),
    ]
