# Generated by Django 5.1.2 on 2024-11-02 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0004_remove_job_listing_timing_delete_timing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]