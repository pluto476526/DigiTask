# Generated by Django 5.1.2 on 2024-11-05 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0013_feedback_job'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='username',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='job_listing',
            old_name='creator',
            new_name='created_by',
        ),
    ]