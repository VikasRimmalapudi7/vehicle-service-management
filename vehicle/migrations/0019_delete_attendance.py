# Generated by Django 5.1.4 on 2024-12-11 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0018_mechanic_subscription_end_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]