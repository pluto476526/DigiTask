# Generated by Django 5.1.2 on 2024-11-17 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0027_notification_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_listing',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]