# Generated by Django 5.1.2 on 2024-11-03 02:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0012_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dash.job_listing'),
        ),
    ]
