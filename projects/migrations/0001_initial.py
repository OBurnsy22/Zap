# Generated by Django 3.0.9 on 2020-12-29 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=300)),
            ],
        ),
    ]
