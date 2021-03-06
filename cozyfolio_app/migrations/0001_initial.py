# Generated by Django 2.2 on 2020-01-25 22:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=75)),
                ('lastName', models.CharField(max_length=75)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=255)),
                ('level', models.CharField(default='normal', max_length=50)),
                ('created_at', models.DateField(default=datetime.datetime.now)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
