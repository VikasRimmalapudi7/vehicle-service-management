# Generated by Django 5.1.4 on 2024-12-11 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0016_mechanic_premium'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mechanic',
            name='salary',
        ),
        migrations.AddField(
            model_name='mechanic',
            name='subscription_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mechanic',
            name='subscription_plan',
            field=models.CharField(blank=True, choices=[('1', '1 Month'), ('3', '3 Months'), ('12', '1 Year')], max_length=20, null=True),
        ),
    ]