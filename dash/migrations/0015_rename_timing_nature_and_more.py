# Generated by Django 5.1.2 on 2024-11-06 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0014_rename_username_feedback_created_by_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Timing',
            new_name='Nature',
        ),
        migrations.RenameField(
            model_name='job_listing',
            old_name='timing',
            new_name='nature',
        ),
    ]
