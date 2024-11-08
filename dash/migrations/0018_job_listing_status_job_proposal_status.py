# Generated by Django 5.1.2 on 2024-11-07 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0017_job_proposal_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_listing',
            name='status',
            field=models.CharField(default='pending', max_length=50),
        ),
        migrations.AddField(
            model_name='job_proposal',
            name='status',
            field=models.CharField(default='sent', max_length=50),
        ),
    ]
