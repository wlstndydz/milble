# Generated by Django 3.2.25 on 2024-10-01 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milble_app', '0005_auto_20240929_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='subscriber_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
