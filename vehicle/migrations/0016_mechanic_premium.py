# Generated by Django 5.1.4 on 2024-12-11 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0015_rename_is_premium_mechanic_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechanic',
            name='premium',
            field=models.BooleanField(default=False),
        ),
    ]
